from typing import Type, TypeVar, Union, ByteString, IO, Optional

from tablib.core import Dataset


T = TypeVar('T', bound=Dataset)


def load_dataset(file: Union[IO, str, ByteString], fmt: Optional[str] = None, dataset_class: Type[T] = Dataset) -> T:
	"""
	Shortcut for loading files.

	Args:
		file: File-like object, string or ByteString that stores data.
		fmt: File data format (for example: xlsx).
		dataset_class: Class of Dataset.
	"""
	return dataset_class().load(file, format=fmt)
