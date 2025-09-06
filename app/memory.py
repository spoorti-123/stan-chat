import redis
import json
from .config import settings

class MemoryStore:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def save_message(self, user_id: str, role: str, message: str):
        key = f"chat:{user_id}"
        entry = {"role": role, "message": message}
        self.client.rpush(key, json.dumps(entry))

    def get_history(self, user_id: str, limit: int = 10):
        key = f"chat:{user_id}"
        messages = self.client.lrange(key, -limit, -1)
        return [json.loads(m) for m in messages]

    def clear_history(self, user_id: str):
        key = f"chat:{user_id}"
        self.client.delete(key)
