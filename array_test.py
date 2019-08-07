from .array import as_chunks, ensure_iterable


def test_as_chunks():
	def collect(x):
		ret = []
		for i in x: ret.append(i)
		return ret
	assert collect(as_chunks([], 5)) == []
	assert collect(as_chunks([1,2,3], 5)) == [[1,2,3]]
	assert collect(as_chunks([1,2,3], 2)) == [[1,2],[3]]
	assert collect(as_chunks([1,2,3], 1)) == [[1],[2],[3]]


def test_ensure_iterable():
	assert ensure_iterable(1) == (1,)
	assert ensure_iterable('x') == ('x',)
	assert ensure_iterable(['x']) == ['x']
	assert ensure_iterable(('x', 'y')) == ('x', 'y')
