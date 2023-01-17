from .array import as_chunks, ensure_iterable

from functools import reduce
from operator import add

import pytest
from hypothesis import given
from hypothesis.strategies import lists, integers


def _collect(x):
	return list(x)


def _flatten(arr):
	return reduce(add, arr, [])


@pytest.mark.parametrize(
	"sequence, chunk_size, expected_result",
	[
		([], 5, []),
		([1, 2, 3], 5, [[1, 2, 3]]),
		([1, 2, 3], 2, [[1, 2], [3]]),
		([1, 2, 3], 1, [[1], [2], [3]]),
	]
)
def test_as_chunks(sequence, chunk_size, expected_result):
	assert _collect(as_chunks(sequence, chunk_size)) == expected_result


@given(lists(integers()), integers(min_value=1))
def test_as_chunks_correctness(source, x):
	_test_as_chunks(source, x)


@given(lists(integers(), max_size=10), integers(min_value=1, max_value=20))
def test_as_chunks_smallscale(source, x):
	_test_as_chunks(source, x)


def _test_as_chunks(source, x):
	result = _collect(as_chunks(source, x))
	num_short = 0
	last_short = False

	for e in result:
		assert len(e) <= x

		if len(e) < x:
			num_short += 1
			last_short = True

	assert num_short <= 1

	if num_short > 0:
		assert last_short

	assert _flatten(result) == source


@pytest.mark.parametrize(
	"src, exp",
	[
		(1, (1,)),
		('x', ('x',)),
		(['x'], ['x']),
		(('x', 'y'), ('x', 'y')),
	]
)
def test_ensure_iterable(src, exp):
	assert ensure_iterable(src) == exp
