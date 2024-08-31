from threading import Thread

import litserve as ls
import torch
from litserve.specs.openai import ChatCompletionRequest
from qwen_vl_utils import process_vision_info
from transformers import (
    AutoProcessor,
    BitsAndBytesConfig,
    Qwen2VLForConditionalGeneration,
    TextIteratorStreamer,
)

from src.config import DEFAULT_MODEL, QWEN2_VL_MODELS


class Qwen2VLAPI(ls.LitAPI):
    def setup(self, device, model_id=DEFAULT_MODEL):
        if model_id not in QWEN2_VL_MODELS.values():
            raise ValueError(f"Invalid model ID: {model_id}")

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            _attn_implementation="flash_attention_2",
            device_map="auto",
            # quantization_config=quantization_config,
        ).eval()

        self.processor = AutoProcessor.from_pretrained(model_id)
        self.streamer = TextIteratorStreamer(
            self.processor.tokenizer,
            skip_prompt=True,
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        )
        self.device = device
        self.model_id = model_id

    def decode_request(self, request: ChatCompletionRequest, context: dict):
        # load model if different from the active model
        if request.model != self.model_id:
            self.setup(self.device, request.model)

        context["generation_args"] = {
            "max_new_tokens": request.max_tokens if request.max_tokens else 2048,
        }

        messages = [
            message.model_dump(exclude_none=True) for message in request.messages
        ]

        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        ).to(self.device)

        return inputs

    def predict(self, model_inputs, context: dict):
        generation_kwargs = dict(
            model_inputs,
            streamer=self.streamer,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            **context["generation_args"],
        )
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        
        for text in self.streamer:
            yield text


if __name__ == "__main__":
    api = Qwen2VLAPI()
    server = ls.LitServer(api, spec=ls.OpenAISpec())
    server.run(port=8000)
