import uuid
from typing import Optional, Any, Dict
from .config import settings

class MemoryCache:
    def __init__(self):
        self._data: Dict[str, Any] = {}
    
    def set(self, key: str, value: Any):
        self._data[key] = value
    
    def get(self, key: str) -> Optional[Any]:
        return self._data.get(key)
    
    def keys(self, pattern: str) -> list:
        pattern = pattern.replace('*', '')
        return [k for k in self._data.keys() if pattern in k]
    
    def delete(self, *keys: str):
        for key in keys:
            self._data.pop(key, None)
    
    def expire(self, key: str, seconds: int):
        pass

class CacheManager:
    def __init__(self):
        try:
            import redis
            self.client = redis.from_url(settings.redis_url, decode_responses=False)
            self.client.ping()
        except Exception:
            self.client = MemoryCache()

    def generate_session_id(self) -> str:
        return str(uuid.uuid4())

    def set_questions(self, session_id: str, questions: list):
        self.client.set(f"session:{session_id}:questions", str(questions))

    def get_questions(self, session_id: str) -> Optional[list]:
        data = self.client.get(f"session:{session_id}:questions")
        if data:
            import ast
            if isinstance(data, bytes):
                data = data.decode('utf-8')
            return ast.literal_eval(data)
        return None

    def set_docx_bytes(self, key: str, bytes_data: bytes):
        self.client.set(key, bytes_data)

    def get_docx_bytes(self, key: str) -> Optional[bytes]:
        return self.client.get(key)

    def delete_session(self, session_id: str):
        keys = self.client.keys(f"session:{session_id}:*")
        if keys:
            self.client.delete(*keys)

    def expire_session(self, session_id: str, seconds: int = 3600):
        keys = self.client.keys(f"session:{session_id}:*")
        for key in keys:
            self.client.expire(key, seconds)

cache_manager = CacheManager()