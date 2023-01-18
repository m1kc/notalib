from typing import Iterable, Any, Sequence, Generator


def as_chunks(arr: Sequence, n: int) -> Generator:
	"""
	Yield successive n-sized chunks from sequence.
	"""
	assert n >= 1

	for i in range(0, len(arr), n):
		yield arr[i:i + n]


def ensure_iterable(x: Any) -> Iterable:
	"""
	Keeps iterable things like lists intact, turns single values into single-element lists. Useful for functions that
	can accept both.
	"""
	excluded_types = [str, bytes]
	has_excluded_type = any(map(lambda t: isinstance(x, t), excluded_types))

	if isinstance(x, Iterable) and not has_excluded_type:
		return x

	return (x,)
