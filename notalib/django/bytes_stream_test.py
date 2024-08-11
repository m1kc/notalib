from notalib.django.bytes_stream import get_stream_bytes_response

from io import BytesIO

from django.http import StreamingHttpResponse, FileResponse


class FakeRequest:
	def __init__(self, http_range: str = "") -> None:
		self.META = {"HTTP_RANGE": http_range}


class TestGetStreamBytesResponse:
	def test_range_mismatch(self):
		buffer = BytesIO(b"deadbee")

		# Function ignores end of range
		response = get_stream_bytes_response(buffer, FakeRequest("bytes = 0 - 5"), "application/octet-stream")
		assert isinstance(response, StreamingHttpResponse)
		assert list(response.streaming_content) == [b"deadbee"]
		assert response.headers.get("Content-Type") == "application/octet-stream"

		response = get_stream_bytes_response(buffer, FakeRequest("bytes = 4 - 999"), "application/octet-stream")
		assert isinstance(response, StreamingHttpResponse)
		assert list(response.streaming_content) == [b"bee"]

	def test_range_match(self):
		response = get_stream_bytes_response(BytesIO(), FakeRequest(), "application/octet-stream")
		assert isinstance(response, FileResponse)
		assert response.headers.get("Content-Type") == "application/octet-stream"
