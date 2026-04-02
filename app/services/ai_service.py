import json
import re
from decimal import Decimal
from urllib import error, request

from app.core.config import settings
from app.models.product import Product
from app.utils.decorators import performance_logger, retry


class AIService:
	"""Service for AI-powered product enrichment."""

	@staticmethod
	@performance_logger
	@retry(attempts=3)
	def generate(product: Product) -> dict[str, str]:
		"""Generate a normalized description and category for a product."""
		payload = {
			"model": settings.AI_MODEL,
			"messages": [
				{
					"role": "system",
					"content": (
						"You are a product enrichment assistant. "
						"Respond with ONLY valid JSON object with keys: "
						"description and category."
					),
				},
				{
					"role": "user",
					"content": (
						f"name: {product.name}\n"
						f"price: {AIService._to_float(product.price)}\n"
						f"details: {product.details}"
					),
				},
			],
			"temperature": 0.2,
		}

		response_text = AIService._chat_completion(payload)
		result = AIService._safe_parse_json(response_text)
		description = str(result.get("description", "")).strip()
		category = str(result.get("category", "")).strip()

		if not description or not category:
			raise ValueError("AI response missing required keys: description/category")

		return {
			"description": description,
			"category": category,
		}

	@staticmethod
	def _chat_completion(payload: dict) -> str:
		provider = settings.AI_PROVIDER.lower().strip()
		if provider == "groq":
			api_key = settings.GROQ_API_KEY
			url = "https://api.groq.com/openai/v1/chat/completions"
		elif provider == "openai":
			api_key = settings.OPENAI_API_KEY
			base_url = settings.OPENAI_BASE_URL.rstrip("/")
			url = f"{base_url}/chat/completions"
		else:
			raise ValueError("Unsupported AI_PROVIDER. Use 'groq' or 'openai'.")

		if not api_key:
			raise ValueError("Missing API key for selected AI provider")

		body = json.dumps(payload).encode("utf-8")
		req = request.Request(
			url=url,
			data=body,
			headers={
				"Authorization": f"Bearer {api_key}",
				"Content-Type": "application/json",
			},
			method="POST",
		)

		try:
			with request.urlopen(req, timeout=20) as resp:  # noqa: S310 - controlled URL
				raw = resp.read().decode("utf-8")
		except error.HTTPError as exc:
			detail = exc.read().decode("utf-8", errors="ignore")
			raise ValueError(f"AI HTTP error {exc.code}: {detail}") from exc
		except error.URLError as exc:
			raise ValueError(f"AI connection error: {exc.reason}") from exc

		try:
			parsed = json.loads(raw)
			return parsed["choices"][0]["message"]["content"]
		except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
			raise ValueError("Invalid AI completion payload format") from exc

	@staticmethod
	def _safe_parse_json(text: str) -> dict:
		"""Parse JSON safely, tolerating markdown wrappers or extra text."""
		candidate = text.strip()

		# First pass: direct parse for strict JSON responses.
		try:
			obj = json.loads(candidate)
			if isinstance(obj, dict):
				return obj
		except json.JSONDecodeError:
			pass

		# Second pass: extract fenced or inline object body.
		match = re.search(r"\{[\s\S]*\}", candidate)
		if not match:
			raise ValueError("AI response is not valid JSON")

		try:
			obj = json.loads(match.group(0))
		except json.JSONDecodeError as exc:
			raise ValueError("AI JSON parsing failed") from exc

		if not isinstance(obj, dict):
			raise ValueError("AI response JSON must be an object")
		return obj

	@staticmethod
	def _to_float(value: Decimal | float | int | str) -> float:
		if isinstance(value, Decimal):
			return float(value)
		return float(value)

