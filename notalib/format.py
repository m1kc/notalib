from typing import Sequence, Optional, List


# Alias of universal function for backward compatibility
def format_long_list(value: List[str], prefix: Optional[str] = None, max_items: Optional[int] = None) -> str:
	return format_long_seq(value, prefix, max_items)


def format_long_seq(value: Sequence[str], prefix: Optional[str] = None, max_items: Optional[int] = None) -> str:
	"""
	Represents a sequence in compact form.

	Args:
		value: Source sequence which will be formatted.
		prefix: The prefix to be set before the sequence.
		max_items: Maximum number of elements in the transformed sequence.
			By default, hides 75% of sequence.

	Returns:
		Compact sequence representation.
	"""
	ret = ''

	if prefix is not None:
		ret = prefix

	if max_items is None:		# For interface backward compatibility. max_items as None is not supported but defined.
		max_items = round(len(value) * 0.25)

	leftover = 0

	if len(value) > max_items:
		leftover = len(value) - max_items
		value = value[:max_items]

	ret += ', '.join(value)

	if leftover > 0:
		ret += f' ...and {leftover} more'

	return ret
