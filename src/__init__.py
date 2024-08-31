from src.config import QWEN2_VL_MODELS


def is_valid_model(model_name: str) -> bool:
    return model_name in QWEN2_VL_MODELS
