from .timedelta import convert_timedelta

from datetime import timedelta

import pytest


TIMEDELTA_FORMATS = ['s', 'ms']


@pytest.mark.parametrize(
	'src_timedelta, fmt, expected_result',
	[
		(timedelta(seconds=15), 's', 15),
		(timedelta(seconds=15), 'ms', 15000),
		(timedelta(milliseconds=11), 's', 0.011),
		(timedelta(milliseconds=11), 'ms', 11),
		(timedelta(microseconds=1), 's', 0.000001),
		(timedelta(microseconds=1), 'ms', 0.001),
		(timedelta(seconds=1, milliseconds=23), 's', 1.023),
		(timedelta(seconds=1, milliseconds=23), 'ms', 1023),
		(timedelta(minutes=-1), 's', -60),
		(timedelta(days=-1), 'Unexpected format', None),
	]
)
def test_convert_timedelta(src_timedelta, fmt, expected_result):
	if fmt not in TIMEDELTA_FORMATS:
		with pytest.raises(NotImplementedError):
			convert_timedelta(src_timedelta, fmt)

	else:
		assert convert_timedelta(src_timedelta, fmt) == pytest.approx(expected_result, 0.1)
