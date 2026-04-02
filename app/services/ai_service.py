import json
import re
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
		"""Generate a catchy 2-sentence description and category from product name."""
		payload = {
			"model": settings.AI_MODEL,
			"messages": [
				{
					"role": "system",
					"content": (
						"You are a product enrichment assistant. "
						"Return ONLY valid JSON object. No markdown, no extra text. "
						"Required keys: description, category. "
						"description must be catchy and exactly 2 sentences. "
						"category must be a short category label."
					),
				},
				{
					"role": "user",
					"content": f"Product name: {product.name}",
				},
			],
			"response_format": {"type": "json_object"},
			"temperature": 0.2,
		}

		response_text = AIService._chat_completion(payload)
		result = AIService._safe_parse_json(response_text)
		return AIService._normalize_output(result, product)

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
	def _normalize_output(result: dict, product: Product) -> dict[str, str]:
		"""Normalize model outputs to strict description/category contract."""
		description_candidates = [
			result.get("description"),
			result.get("summary"),
			result.get("details"),
			result.get("content"),
			result.get("tagline"),
		]
		category_candidates = [
			result.get("category"),
			result.get("type"),
			result.get("segment"),
		]

		raw_description = next((str(v).strip() for v in description_candidates if v), "")
		raw_category = next((str(v).strip() for v in category_candidates if v), "")

		defaults = AIService.default_content_from_name(product.name)
		description = AIService._ensure_two_sentences(raw_description, product.name)
		category = AIService._sanitize_category(raw_category)

		if not description:
			description = defaults["description"]
		if not category:
			category = defaults["category"]

		return {
			"description": description,
			"category": category,
		}

	@staticmethod
	def default_content_from_name(name: str) -> dict[str, str]:
		"""Create strict fallback content from name only."""
		product_name = name.strip() or "This product"
		description = (
			f"{product_name} brings standout style and everyday value in one compelling package. "
			f"Choose {product_name} to elevate your routine with confidence and convenience."
		)
		category = AIService._infer_category_from_name(product_name)
		return {"description": description, "category": category}

	@staticmethod
	def _ensure_two_sentences(text: str, product_name: str) -> str:
		"""Return exactly two readable sentences."""
		cleaned = re.sub(r"\s+", " ", text).strip()
		sentences = [
			s.strip()
			for s in re.split(r"(?<=[.!?])\s+", cleaned)
			if s.strip()
		]

		if len(sentences) >= 2:
			first = AIService._with_terminal_punctuation(sentences[0])
			second = AIService._with_terminal_punctuation(sentences[1])
			return f"{first} {second}"

		if len(sentences) == 1:
			first = AIService._with_terminal_punctuation(sentences[0])
			second = f"{product_name} is designed to make a strong impression every day."
			return f"{first} {second}"

		return AIService.default_content_from_name(product_name)["description"]

	@staticmethod
	def _with_terminal_punctuation(text: str) -> str:
		if text.endswith((".", "!", "?")):
			return text
		return f"{text}."

	@staticmethod
	def _sanitize_category(category: str) -> str:
		cleaned = re.sub(r"[^A-Za-z0-9\- /]", "", category).strip()
		if not cleaned:
			return ""
		return cleaned[:40].title()

	@staticmethod
	def _infer_category_from_name(name: str) -> str:
		lower = name.lower()
		if any(k in lower for k in ["laptop", "phone", "tablet", "headphone", "camera", "monitor"]):
			return "Electronics"
		if any(k in lower for k in ["shirt", "shoe", "jacket", "bag", "watch"]):
			return "Fashion"
		if any(k in lower for k in ["sofa", "chair", "lamp", "kitchen", "bottle"]):
			return "Home"
		if any(k in lower for k in ["book", "notebook", "pen"]):
			return "Stationery"
		return "General"

