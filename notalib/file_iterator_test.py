from notalib.file_iterator import file_iterator

from io import BytesIO

import pytest


class TestFileIterator:
	def test_with_empty_buffer(self):
		buffer = BytesIO()

		with pytest.raises(StopIteration):
			next(file_iterator(buffer))

	def test_chunk_size(self):
		buffer = BytesIO(b"deadbee")

		assert list(file_iterator(buffer, chunk_size=1)) == [b"d", b"e", b"a", b"d", b"b", b"e", b"e"]
		assert list(file_iterator(buffer, chunk_size=7)) == [b"deadbee"]

	def test_offset(self):
		buffer = BytesIO(b"deadbee")

		assert list(file_iterator(buffer, chunk_size=7)) == [b"deadbee"]
		assert list(file_iterator(buffer, chunk_size=7, offset=0)) == [b"deadbee"]
		assert list(file_iterator(buffer, chunk_size=7, offset=4)) == [b"bee"]

	def test_length(self):
		buffer = BytesIO(b"deadbee")

		assert list(file_iterator(buffer, chunk_size=7)) == [b"deadbee"]
		assert list(file_iterator(buffer, chunk_size=7, length=7)) == [b"deadbee"]
		assert list(file_iterator(buffer, chunk_size=7, length=4)) == [b"dead"]
