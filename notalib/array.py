from typing import Iterable, TypeVar, Generator, Tuple
from itertools import islice


T = TypeVar('T')


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


def batched(iterable: Iterable[T], n: int) -> Generator[Tuple[T, ...], None, None]:
	"""
	Batch data from the iterable into tuples of length n.

	Args:
		iterable: An iterable to batch.
		n: Batch size.

	Notes:
		* Src: https://docs.python.org/3.12/library/itertools.html#itertools.batched

	Examples:
		>>> list(batched('ABCDEFG', 3))
		... [('A', 'B', 'C'), ('D', 'E', 'F'), ('G', )]
	"""
	if n < 1:
		raise ValueError('n must be at least one')

	it = iter(iterable)
	batch = tuple(islice(it, n))

	while batch:
		yield batch
		batch = tuple(islice(it, n))
