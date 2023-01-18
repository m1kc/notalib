from typing import Optional, TypeVar


ComparedObject = TypeVar('ComparedObject')


class Range:
	"""
	Representation of a range with the possibility of separating the intersection of two ranges.

	Notes:
		Unlike most libraries (and the standard library), this one works with most
		generic definition of range. Range is defined as just anything that
		has start and end. The only requirement is for these values to be comparable.
		So, this works with ints, timestamps, tuples, whatever.

	Examples:
		>>> a, b = Range(11, 15), Range(10, 14)
		>>> a.get_overlapped_range(b)
		Range(11, 14)

	Source: https://stackoverflow.com/a/48265052
	"""
	def __init__(self, start: ComparedObject, end: ComparedObject) -> None:
		self.start = start
		self.end = end

	def is_overlapped(self, other_range: 'Range') -> bool:
		return max(self.start, other_range.start) < min(self.end, other_range.end)

	def get_overlapped_range(self, other_range: 'Range') -> Optional['Range']:
		if not self.is_overlapped(other_range):
			return

		if other_range.start >= self.start:
			if self.end >= other_range.end:
				return Range(other_range.start, other_range.end)
			return Range(other_range.start, self.end)

		else:
			if other_range.end >= self.end:
				return Range(self.start, self.end)
			return Range(self.start, other_range.end)

	def __eq__(self, other: 'Range') -> bool:
		return self.start == other.start and self.end == other.end

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.start} - {self.end})"
