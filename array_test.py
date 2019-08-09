from .array import as_chunks, ensure_iterable

from hypothesis import given
from hypothesis.strategies import lists, integers


def _collect(x):
	ret = []
	for i in x: ret.append(i)
	return ret


def _flatten(arr):
	ret = []
	for subarr in arr:
		for elem in subarr:
			ret.append(elem)
	return ret


def test_as_chunks():
	assert _collect(as_chunks([], 5)) == []
	assert _collect(as_chunks([1,2,3], 5)) == [[1,2,3]]
	assert _collect(as_chunks([1,2,3], 2)) == [[1,2],[3]]
	assert _collect(as_chunks([1,2,3], 1)) == [[1],[2],[3]]


@given(lists(integers()), integers(min_value=1))
def test_as_chunks_correctness(source, x):
	result = _collect(as_chunks(source, x))
	for e in result:
		assert len(e) <= x
	assert(_flatten(result) == source)


@given(lists(integers(), max_size=10), integers(min_value=1, max_value=20))
def test_as_chunks_smallscale(source, x):
	result = _collect(as_chunks(source, x))
	for e in result:
		assert len(e) <= x
	assert(_flatten(result) == source)


def test_ensure_iterable():
	assert ensure_iterable(1) == (1,)
	assert ensure_iterable('x') == ('x',)
	assert ensure_iterable(['x']) == ['x']
	assert ensure_iterable(('x', 'y')) == ('x', 'y')
