from datetime import timedelta
from typing import Union
from typing_extensions import Literal


TimedeltaFormat = Literal['s', 'ms']


def convert_timedelta(src: timedelta, fmt: TimedeltaFormat) -> Union[float, int]:
	"""
	Converts standard timedelta object to specified format.

	Args:
		src: Source timedelta which will be converted.
		fmt: The desired format to convert the timedelta.

	Raises:
		NotImplementedError: If an unsupported format is specified.
	"""
	if fmt == 's':
		return src.total_seconds()
	elif fmt == 'ms':
		return src.total_seconds() * 1000

	raise NotImplementedError(f"Timedelta conversion to '{fmt}' format is not implemented")
