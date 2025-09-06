import asyncio
import httpx
from abc import ABC, abstractmethod
from .config import settings

class LLMClient(ABC):
    @abstractmethod
    async def generate(self, user_id: str, message: str) -> tuple[str, str]:
        """Return (reply, model_name)"""

class DummyClient(LLMClient):
    async def generate(self, user_id: str, message: str) -> tuple[str, str]:
        reply = f"(stub) You said: {message}. I’m live and wired for Phase 1."
        return reply, "dummy-echo"

class OpenAIClient(LLMClient):
    def __init__(self) -> None:
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    async def generate(self, user_id: str, message: str) -> tuple[str, str]:
        # sync SDK → run in thread to keep FastAPI async-friendly
        def _call():
            return self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": settings.SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
            )
        resp = await asyncio.to_thread(_call)
        text = resp.choices[0].message.content
        return text, self.model

class HFClient(LLMClient):
    def __init__(self) -> None:
        self.token = settings.HF_API_KEY
        self.model = settings.HF_MODEL
        self.url = f"https://api-inference.huggingface.co/models/{self.model}"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    async def generate(self, user_id: str, message: str) -> tuple[str, str]:
        payload = {
            "inputs": f"{settings.SYSTEM_PROMPT}\nUser: {message}\nAssistant:",
            "parameters": {"max_new_tokens": 256, "temperature": 0.7}
        }
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(self.url, headers=self.headers, json=payload)
            r.raise_for_status()
            data = r.json()
            # HF can return either list[{'generated_text': ...}] or TGI-style objects
            if isinstance(data, list) and data and "generated_text" in data[0]:
                text = data[0]["generated_text"].split("Assistant:", 1)[-1].strip()
            else:
                # fallback for other server shapes
                text = str(data)
        return text, self.model

def make_client() -> LLMClient:
    if settings.PROVIDER == "openai":
        return OpenAIClient()
    if settings.PROVIDER == "hf":
        return HFClient()
    return DummyClient()
