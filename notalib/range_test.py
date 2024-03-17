from notalib.range import Range

from typing import Optional
from datetime import datetime
from functools import reduce
from operator import eq, attrgetter

import pytest


def ranges_are_equal(*args: Range) -> bool:
	return reduce(eq, map(attrgetter('start'), args)) and reduce(eq, map(attrgetter('end'), args))



class TestRange:
	def test___init__(self):
		r = Range(23, 2)
		assert r.start == 23 and r.end == 2

	@pytest.mark.parametrize(
		"first, second, is_overlapped",
		[
			(Range(1, 5), Range(5, 10), False),
			(Range(5, 10), Range(1, 5), False),
			(Range(1, 5), Range(-1, 3), True),
			(Range(1, 5), Range(3, 10), True),
			(Range(1, 5), Range(0, 10), True),

			(
				Range(datetime(2024, 1, 1, 15, 15, 15), datetime(2024, 1, 1, 15, 15, 15)),
				Range(datetime(2024, 1, 1, 23, 23, 23), datetime(2024, 1, 1, 23, 23, 23)),
				False,
			),
			(
				Range(datetime(2024, 1, 1, 15, 15, 15), datetime(2024, 1, 1, 20, 20, 20)),
				Range(datetime(2024, 1, 1, 18, 18, 18), datetime(2024, 1, 1, 23, 23, 23)),
				True,
			),

			(Range((1, 1), (1, 5)), Range((2, 1), (2, 5)), False),
			(Range((1, 1), (1, 5)), Range((1, 2), (2, 5)), True),
		],
	)
	def test_is_overlapped(self, first: Range, second: Range, is_overlapped: bool):
		assert first.is_overlapped(second) == is_overlapped

	@pytest.mark.parametrize(
		"first, second, expected_result",
		[
			(Range(1, 5), Range(5, 10), None),
			(Range(1, 5), Range(1, 3), Range(1, 3)),
			(Range(1, 5), Range(3, 5), Range(3, 5)),
			(Range(4, 8), Range(1, 6), Range(4, 6)),
			(Range(4, 8), Range(6, 10), Range(6, 8)),
			(Range(4, 8), Range(1, 10), Range(4, 8)),
		],
	)
	def test_get_overlapped_range(self, first: Range, second: Range, expected_result: Optional[Range]):
		result = first.get_overlapped_range(second)

		if expected_result is None:
			assert result is None

		else:
			assert ranges_are_equal(result, expected_result)
