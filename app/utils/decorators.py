import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar


F = TypeVar("F", bound=Callable[..., Any])
logger = logging.getLogger(__name__)


def performance_logger(func: F) -> F:
	"""Log execution time for decorated callables."""

	@wraps(func)
	def wrapper(*args: Any, **kwargs: Any) -> Any:
		start = time.perf_counter()
		try:
			return func(*args, **kwargs)
		finally:
			duration_ms = (time.perf_counter() - start) * 1000
			logger.info("%s executed in %.2fms", func.__name__, duration_ms)

	return wrapper  # type: ignore[return-value]


def retry(attempts: int = 3, delay_seconds: float = 0.5) -> Callable[[F], F]:
	"""Retry a callable a fixed number of attempts."""

	if attempts < 1:
		raise ValueError("attempts must be >= 1")

	def decorator(func: F) -> F:
		@wraps(func)
		def wrapper(*args: Any, **kwargs: Any) -> Any:
			last_error: Exception | None = None
			for attempt in range(1, attempts + 1):
				try:
					return func(*args, **kwargs)
				except Exception as exc:  # noqa: BLE001 - retry logic needs broad catch
					last_error = exc
					if attempt == attempts:
						raise
					logger.warning(
						"%s failed on attempt %s/%s: %s",
						func.__name__,
						attempt,
						attempts,
						exc,
					)
					time.sleep(delay_seconds)

			if last_error is not None:
				raise last_error
			raise RuntimeError("retry failed without capturing an exception")

		return wrapper  # type: ignore[return-value]

	return decorator

