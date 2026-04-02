_cache: dict[str, object] = {}


def get_cache(key: str) -> object | None:
	return _cache.get(key)


def set_cache(key: str, value: object) -> None:
	_cache[key] = value

