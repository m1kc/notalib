from notalib.range import Range, InfiniteRange

from typing import Optional
from datetime import datetime, date
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


class TestInfiniteRange:
	def test___init__(self):
		r = InfiniteRange()
		assert r.start is None and r.end is None
		r = InfiniteRange(23, 2)
		assert r.start == 23 and r.end == 2
		r = InfiniteRange(date(2024, 1, 1), date(2024, 12, 31))
		assert r.start == date(2024, 1, 1) and r.end == date(2024, 12, 31)

	def test___hash__(self):
		r = InfiniteRange(12, 31)
		assert hash((12, 31)) == r.__hash__()

	def test___contains__(self):
		r = InfiniteRange()
		assert 12 in r
		assert date(2024, 1, 1) in r

		r = InfiniteRange(None, 15)
		assert 12 in r
		assert 16 not in r

		r = InfiniteRange(15, None)
		assert 12 not in r
		assert 16 in r

		r = InfiniteRange(15, 15)
		assert 12 not in r
		assert 15 in r
		assert 16 not in r

	@pytest.mark.parametrize(
		"origin, other, expected_result",
		[
			(InfiniteRange(), 12, False),
			(InfiniteRange(), InfiniteRange(None, 15), False),
			(InfiniteRange(), InfiniteRange(15, None), False),
			(InfiniteRange(), InfiniteRange(15, 15), False),
			(InfiniteRange(), InfiniteRange(None, None), True),
			(InfiniteRange(15, None), InfiniteRange(15, None), True),
			(InfiniteRange(None, 15), InfiniteRange(None, 15), True),
			(InfiniteRange(15, 15), InfiniteRange(15, 15), True),
			(InfiniteRange(15, 15), InfiniteRange(date(2024, 1, 1), date(2024, 12, 31)), False),
			(
				InfiniteRange(date(2024, 1, 1), date(2024, 12, 31)),
				InfiniteRange(date(2024, 1, 1), date(2024, 12, 31)),
				True,
			),
		],
	)
	def test___eq__(self, origin, other, expected_result):
		assert (origin == other) == expected_result

	def test___repr__(self):
		assert InfiniteRange().__repr__() == "InfiniteRange [None:None]"
		assert InfiniteRange(15, None).__repr__() == "InfiniteRange [15:None]"
		assert InfiniteRange(None, 15).__repr__() == "InfiniteRange [None:15]"
		assert InfiniteRange(15, 15).__repr__() == "InfiniteRange [15:15]"

	def test___str__(self):
		assert InfiniteRange().__str__() == "None:None"
		assert InfiniteRange(15, None).__str__() == "15:None"
		assert InfiniteRange(None, 15).__str__() == "None:15"
		assert InfiniteRange(15, 15).__str__() == "15:15"

	@pytest.mark.parametrize(
		"origin, other, expected_result",
		[
			# Range-specific tests
			(InfiniteRange(1, 5), InfiniteRange(5, 10), True),
			(InfiniteRange(5, 10), InfiniteRange(1, 5), True),
			(InfiniteRange(1, 5), InfiniteRange(-1, 3), True),
			(InfiniteRange(1, 5), InfiniteRange(3, 10), True),
			(InfiniteRange(1, 5), InfiniteRange(0, 10), True),
			(
				InfiniteRange(datetime(2024, 1, 1, 15, 15, 15), datetime(2024, 1, 1, 15, 15, 15)),
				InfiniteRange(datetime(2024, 1, 1, 23, 23, 23), datetime(2024, 1, 1, 23, 23, 23)),
				False,
			),
			(
				InfiniteRange(datetime(2024, 1, 1, 15, 15, 15), datetime(2024, 1, 1, 20, 20, 20)),
				InfiniteRange(datetime(2024, 1, 1, 18, 18, 18), datetime(2024, 1, 1, 23, 23, 23)),
				True,
			),
			(InfiniteRange((1, 1), (1, 5)), InfiniteRange((2, 1), (2, 5)), False),
			(InfiniteRange((1, 1), (1, 5)), InfiniteRange((1, 2), (2, 5)), True),

			# InfiniteRange-specific tests
			(InfiniteRange(), InfiniteRange(), True),
			(InfiniteRange(), Range(15, 15), True),
			(InfiniteRange(), InfiniteRange(15, 15), True),
			(InfiniteRange(), InfiniteRange(date(2024, 1, 1), date(2024, 12, 31)), True),
			(InfiniteRange(None, 15), InfiniteRange(10, 20), True),
			(InfiniteRange(None, 15), InfiniteRange(15, 20), True),
			(InfiniteRange(None, 15), InfiniteRange(16, 20), False),
			(InfiniteRange(15, None), InfiniteRange(10, 20), True),
			(InfiniteRange(15, None), InfiniteRange(10, 15), True),
			(InfiniteRange(15, None), InfiniteRange(10, 14), False),
			(InfiniteRange(None, date(2024, 1, 1)), InfiniteRange(date(2024, 12, 31), None), False),
			(InfiniteRange(None, 15), InfiniteRange(None, 20), True),
			(InfiniteRange(15, None), InfiniteRange(20, None), True),
			(InfiniteRange(10, 15), InfiniteRange(20, None), False),
			(InfiniteRange(25, 30), InfiniteRange(None, 20), False),
		],
	)
	def test_is_overlapped(self, origin, other, expected_result):
		assert origin.is_overlapped(other) == expected_result

	@pytest.mark.parametrize(
		"origin, other, expected_result",
		[
			# Range-specific tests
			(InfiniteRange(1, 5), InfiniteRange(5, 10), InfiniteRange(5, 5)),
			(InfiniteRange(1, 5), InfiniteRange(1, 3), InfiniteRange(1, 3)),
			(InfiniteRange(1, 5), InfiniteRange(3, 5), InfiniteRange(3, 5)),
			(InfiniteRange(4, 8), InfiniteRange(1, 6), InfiniteRange(4, 6)),
			(InfiniteRange(4, 8), InfiniteRange(6, 10), InfiniteRange(6, 8)),
			(InfiniteRange(4, 8), InfiniteRange(1, 10), InfiniteRange(4, 8)),

			# InfiniteRange-specific tests
			(InfiniteRange(), InfiniteRange(), InfiniteRange()),
			(InfiniteRange(10, 20), InfiniteRange(), InfiniteRange(10, 20)),
			(InfiniteRange(), InfiniteRange(10, 20), InfiniteRange(10, 20)),
			(InfiniteRange(10, 20), InfiniteRange(10, 20), InfiniteRange(10, 20)),
			(InfiniteRange(None, 20), InfiniteRange(10, 30), InfiniteRange(10, 20)),
			(InfiniteRange(None, 20), InfiniteRange(20, 30), InfiniteRange(20, 20)),
			(InfiniteRange(None, 20), InfiniteRange(25, 30), None),
			(InfiniteRange(20, None), InfiniteRange(10, 30), InfiniteRange(20, 30)),
			(InfiniteRange(20, None), InfiniteRange(10, 20), InfiniteRange(20, 20)),
			(InfiniteRange(20, None), InfiniteRange(10, 15), None),
			(InfiniteRange(20, 40), Range(25, 35), InfiniteRange(25, 35)),
		],
	)
	def test_get_overlapped_range(self, origin, other, expected_result):
		assert origin.get_overlapped_range(other) == expected_result

	@pytest.mark.parametrize(
		"origin, other, expected_result",
		[
			(InfiniteRange(), InfiniteRange(), InfiniteRange()),
			(InfiniteRange(10, 20), InfiniteRange(), InfiniteRange()),
			(InfiniteRange(), Range(30, 40), InfiniteRange()),
			(InfiniteRange(None, 20), InfiniteRange(30, 40), None),
			(InfiniteRange(None, 20), InfiniteRange(10, 40), InfiniteRange(None, 40)),
			(InfiniteRange(20, None), InfiniteRange(10, 40), InfiniteRange(10, None)),
			(InfiniteRange(20, None), InfiniteRange(None, 40), InfiniteRange()),
			(InfiniteRange(None, 20), InfiniteRange(10, None), InfiniteRange()),
			(InfiniteRange(10, 20), InfiniteRange(None, 30), InfiniteRange(None, 30)),
			(InfiniteRange(10, 20), InfiniteRange(0, None), InfiniteRange(0, None)),
			(
				InfiniteRange(date(2024, 1, 1), date(2024, 6, 30)),
				InfiniteRange(date(2024, 6, 30), date(2024, 12, 31)),
				InfiniteRange(date(2024, 1, 1), date(2024, 12, 31)),
			),
		],
	)
	def test_concat(self, origin, other, expected_result):
		assert origin.concat(other) == expected_result

	@pytest.mark.parametrize(
		"ranges, expected_result",
		[
			([], set()),
			([InfiniteRange()], {InfiniteRange()}),
			([InfiniteRange(), InfiniteRange()], {InfiniteRange()}),
			([InfiniteRange(), InfiniteRange(), InfiniteRange(1, 5)], {InfiniteRange()}),
			([InfiniteRange(1, 5), InfiniteRange()], {InfiniteRange()}),
			([InfiniteRange(1, 5), InfiniteRange(1, 5)], {InfiniteRange(1, 5)}),
			([InfiniteRange(1, 5), InfiniteRange(2, 10)], {InfiniteRange(1, 10)}),
			([InfiniteRange(2, 10), InfiniteRange(1, 5)], {InfiniteRange(1, 10)}),
			(
				[InfiniteRange(None, 10), InfiniteRange(1, 5), InfiniteRange(11, 15)],
				{InfiniteRange(None, 10), InfiniteRange(11, 15)},
			),
			(
				[InfiniteRange(10, 11), InfiniteRange(1, 6), InfiniteRange(7, None), InfiniteRange(6, 7)],
				{InfiniteRange(1, None)},
			),
			(
				[InfiniteRange(None, 1), InfiniteRange(5, None), InfiniteRange(3, 6), InfiniteRange(1, 3)],
				{InfiniteRange(None, None)},
			),
		],
	)
	def test_squash(self, ranges, expected_result):
		assert set(InfiniteRange.squash(*ranges)) == expected_result
