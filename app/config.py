import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # General
    APP_ENV = os.getenv("APP_ENV", "local")
    PROVIDER = os.getenv("PROVIDER", "dummy")

    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # HuggingFace
    HF_API_KEY = os.getenv("HF_API_KEY", "")
    HF_MODEL = os.getenv("HF_MODEL", "HuggingFaceH4/zephyr-7b-beta")

    # Redis (memory layer)
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB = int(os.getenv("REDIS_DB", 0))

    # Prompt
    SYSTEM_PROMPT = os.getenv(
        "SYSTEM_PROMPT",
        "You are a helpful, concise assistant."
    )

settings = Settings()
