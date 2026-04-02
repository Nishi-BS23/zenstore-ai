import json

import redis

from app.core.config import settings


class CacheService:
	"""Redis-backed cache abstraction for product records."""

	def __init__(self) -> None:
		self._client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)

	@staticmethod
	def product_key(product_id: str) -> str:
		return f"product:{product_id}"

	def get(self, key: str) -> dict | None:
		try:
			value = self._client.get(key)
		except redis.RedisError:
			return None
		if value is None:
			return None
		try:
			parsed = json.loads(value)
		except json.JSONDecodeError:
			self.delete(key)
			return None
		return parsed if isinstance(parsed, dict) else None

	def set(self, key: str, value: dict, ttl_seconds: int = 300) -> None:
		try:
			self._client.setex(key, ttl_seconds, json.dumps(value, default=str))
		except redis.RedisError:
			return None

	def delete(self, key: str) -> None:
		try:
			self._client.delete(key)
		except redis.RedisError:
			return None

	def invalidate_product(self, product_id: str) -> None:
		self.delete(self.product_key(product_id))

	def get_product(self, product_id: str) -> dict | None:
		return self.get(self.product_key(product_id))

	def set_product(self, product_id: str, value: dict, ttl_seconds: int = 300) -> None:
		self.set(self.product_key(product_id), value, ttl_seconds=ttl_seconds)