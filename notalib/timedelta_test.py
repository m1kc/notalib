from .timedelta import convert_timedelta, TimedeltaFormat

from datetime import timedelta
from typing_extensions import get_args

import pytest


TIMEDELTA_FORMATS = get_args(TimedeltaFormat)


@pytest.mark.parametrize(
	'src_timedelta, fmt, expected_result',
	[
		(timedelta(seconds=15), 's', 15),
		(timedelta(seconds=15), 'ms', 15000),
		(timedelta(milliseconds=11), 's', 0.011),
		(timedelta(milliseconds=11), 'ms', 11),
		(timedelta(microseconds=1), 's', 0.000001),
		(timedelta(microseconds=1), 'ms', 0.001),
		(timedelta(days=-1), 'Unexpected format', None),
	]
)
def test_convert_timedelta(src_timedelta, fmt, expected_result):
	if fmt not in TIMEDELTA_FORMATS:
		with pytest.raises(NotImplementedError):
			convert_timedelta(src_timedelta, fmt)

	else:
		assert convert_timedelta(src_timedelta, fmt) == pytest.approx(expected_result, 0.1)
