IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".m4v"]
MAX_NUM_FRAMES = 64

SYSTEM_MESSAGE = {
    "role": "system",
    "content": "You are a helpful assistant.",
}

QWEN2_VL_MODELS = {
    "Qwen2-VL-7B": "Qwen/Qwen2-VL-7B-Instruct",
    "Qwen2-VL-2B": "Qwen/Qwen2-VL-2B-Instruct",
}

DEFAULT_MODEL = QWEN2_VL_MODELS["Qwen2-VL-7B"]
