import csv
import io
from collections.abc import Generator
from typing import BinaryIO


def generate_slug(value: str) -> str:
	"""Minimal slug generator placeholder."""
	return value.strip().lower().replace(" ", "-")


def iter_csv_rows(file_obj: BinaryIO) -> Generator[tuple[int, dict[str, str]], None, None]:
	"""Yield CSV rows one by one without loading the entire file in memory."""
	text_stream = io.TextIOWrapper(file_obj, encoding="utf-8", newline="")
	try:
		reader = csv.DictReader(text_stream)
		for row_number, row in enumerate(reader, start=2):
			normalized = {str(k).strip(): (v or "").strip() for k, v in row.items() if k is not None}
			yield row_number, normalized
	finally:
		# Detach so UploadFile can manage the underlying buffer lifecycle.
		text_stream.detach()

