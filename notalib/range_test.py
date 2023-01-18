from .range import Range

from datetime import date, datetime

import pytest


@pytest.mark.parametrize(
	"source_range, other_range, overlapped_range",
	[
		(Range(2022, 2024), Range(2023, 2025), Range(2023, 2024)),
		(Range((12, 15), (12, 57)), Range((12, 34), (15, 16)), Range((12, 34), (12, 57))),
		(
			Range(date(2022, 12, 12), date(2022, 12, 31)),
			Range(date(2022, 12, 24), date(2023, 2, 27)),
			Range(date(2022, 12, 24), date(2022, 12, 31)),
		),
		(
			Range(datetime(2023, 1, 1, 10, 15, 16), datetime(2023, 1, 1, 20, 34, 57)),
			Range(datetime(2023, 1, 1, 12, 16, 42), datetime(2023, 1, 1, 23, 59, 59)),
			Range(datetime(2023, 1, 1, 12, 16, 42), datetime(2023, 1, 1, 20, 34, 57)),
		),
		(Range(11, 15), Range(11, 15), Range(11, 15)),
		(Range(0, 1), Range(3, 4), None),
		(Range(0, 1), Range(1, 5), None),
		(Range(5, 10), Range(1, 6), Range(5, 6)),
	]
)
def test_range(source_range, other_range, overlapped_range):
	assert source_range.get_overlapped_range(other_range) == overlapped_range
