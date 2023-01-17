from typing import Iterable, Any, Sequence, Generator


def as_chunks(seq: Sequence, n: int) -> Generator:
	"""
	Yield successive n-sized chunks from sequence.
	"""
	assert n >= 1

	for i in range(0, len(seq), n):
		yield seq[i:i + n]


def ensure_iterable(x: Any) -> Iterable:
	"""
	Keeps iterable things like lists intact, turns single values into single-element lists. Useful for functions that
	can accept both.

	TODO:
		Add other cases
	"""
	if isinstance(x, list) or isinstance(x, tuple):
		return x

	return (x,)
