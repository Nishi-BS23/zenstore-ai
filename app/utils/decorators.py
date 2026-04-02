from collections.abc import Callable
from typing import Any


def noop_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
	"""Placeholder decorator that returns the original function."""
	return func

