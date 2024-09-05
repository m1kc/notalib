import os
from io import BytesIO
from typing import Optional, Generator


def file_iterator(
	buffer: BytesIO,
	chunk_size: int = 8192,
	offset: int = 0,
	length: Optional[int] = None,
) -> Generator[bytes, None, None]:
	"""
	Iterates over byte buffer and yields chunks of specified size.

	Args:
		buffer: A buffer the data from which you want to split into chunks.
		chunk_size: The size of a single chunk returned during iteration.
		offset: Offset relative to the beginning of a buffer (the size of the content that will not be yielded).
		length: The length of a buffer content that needs to be yielded.

	Returns:
		Generator of buffer content.
	"""
	buffer.seek(offset, os.SEEK_SET)
	remaining = length

	while True:
		bytes_length = (chunk_size if remaining is None else min(remaining, chunk_size))
		data = buffer.read(bytes_length)

		if not data:
			break

		if remaining:
			remaining -= len(data)

		yield data
