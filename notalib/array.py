def as_chunks(arr, n):
	"""
	Yield successive n-sized chunks from arr.
	"""
	assert n >= 1
	for i in range(0, len(arr), n):
		yield arr[i:i + n]


def ensure_iterable(x):
	if isinstance(x, list): return x
	if isinstance(x, tuple): return x
	# TODO other cases
	return (x,)
