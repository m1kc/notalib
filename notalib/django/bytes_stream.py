from notalib.file_iterator import file_iterator

import re
from io import BytesIO
from typing import Union

from django.http.request import HttpRequest
from django.http import StreamingHttpResponse, FileResponse


TypeResponse = Union[StreamingHttpResponse, FileResponse]
# Used for streaming audio files. See: https://www.djangotricks.com/tricks/4S7qbNhtUeAD/
RANGE_RE = re.compile(r"bytes\s*=\s*(\d+)\s*-\s*(\d*)", re.I)


def get_stream_bytes_response(buffer: BytesIO, request: HttpRequest, content_type: str) -> TypeResponse:
	"""
	Returns part of a buffer or a entire buffer, depending on the Range header.

	Args:
		buffer: A buffer whose content needs to be returned in the response.
		request: HttpRequest object.
		content_type: Response content type.
	"""
	size = buffer.getbuffer().nbytes
	range_header = request.META.get("HTTP_RANGE", "").strip()
	range_match = RANGE_RE.match(range_header)

	if range_match:
		first_byte, last_byte = range_match.groups()
		first_byte = int(first_byte) if first_byte else 0
		last_byte = first_byte + 8388608	# 1024 * 1024 * 8

		if last_byte >= size:
			last_byte = size - 1

		length = last_byte - first_byte + 1
		response = StreamingHttpResponse(
			file_iterator(buffer, offset=first_byte, length=length),
			status=206,
			content_type=content_type,
		)
		response['Content-Range'] = f"bytes {first_byte}-{last_byte}/{size}"
		response['Accept-Ranges'] = "bytes"

		return response
	else:
		return FileResponse(buffer, content_type=content_type)
