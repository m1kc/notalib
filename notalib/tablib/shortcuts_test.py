from notalib.tablib.shortcuts import load_dataset

from io import BytesIO

from tablib.core import Dataset


class FakeDataset(Dataset):
	_instance = None

	def __new__(cls, *args, **kwargs) -> "FakeDataset":
		if cls._instance is None:
			cls._instance = super().__new__(cls, *args, **kwargs)

		return cls._instance

	def __init__(self, *args, **kwargs):
		if self.__class__._instance is not None:
			return

		super().__init__(*args, **kwargs)

		self._in_stream = None
		self._format = None
		self._kwargs = {}

	def load(self, in_stream, format=None, **kwargs):
		self._in_stream = in_stream
		self._format = format
		self._kwargs = kwargs

		return "NO DATA"


def test_load_dataset():
	stream = BytesIO()
	fmt = "FORMAT"

	assert load_dataset(stream, fmt, FakeDataset)

	dataset = FakeDataset()
	assert dataset._in_stream is stream
	assert dataset._format is fmt
	assert dataset._kwargs == {}
