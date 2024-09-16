from typing import Optional, Any


class Range(object):
	"""
	Unlike most libraries (and the standard library), this one works with most
	generic definition of range. Range is defined as just anything that
	has start and end. The only requirement is for these values to be comparable.
	So, this works with ints, timestamps, tuples, whatever.

	https://stackoverflow.com/a/48265052
	"""
	def __init__(self, start, end):
		self.start = start
		self.end = end
		# self.duration = self.end - self.start

	def is_overlapped(self, other_range):
		# TODO: Can be simplified
		if max(self.start, other_range.start) < min(self.end, other_range.end):
			return True
		else:
			return False

	def get_overlapped_range(self, other_range):
		if not self.is_overlapped(other_range): return
		if other_range.start >= self.start:
			if self.end >= other_range.end:
				return Range(other_range.start, other_range.end)
			else:
				return Range(other_range.start, self.end)
		elif other_range.start < self.start:
			if other_range.end >= self.end:
				return Range(self.start, self.end)
			else:
				return Range(self.start, other_range.end)

	# def __repr__(self):
	# 	return '{0} ------> {1}'.format(*[time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(d))
	# 		for d in [self.start, self.end]])


class InfiniteRange(Range):
	"""
	Like the Range, but supports infinite bounds represented by None values.

	Notes:
		* The behavior of the `is_overlapped` method differs from that of the `Range` class.
	"""
	def __init__(self, start=None, end=None):
		super().__init__(start, end)

	def __hash__(self) -> int:
		return hash((self.start, self.end))

	def __contains__(self, value) -> bool:
		greater_than_start = True
		less_than_end = True

		if self.start is not None:
			greater_than_start = self.start <= value

		if self.end is not None:
			less_than_end = self.end >= value

		return greater_than_start and less_than_end

	def __eq__(self, other: Any) -> bool:
		return (
			isinstance(other, InfiniteRange)
			and self.start == other.start
			and self.end == other.end
		)

	def __repr__(self) -> str:
		return f"{self.__class__.__qualname__} [{self.start}:{self.end}]"

	def __str__(self) -> str:
		return f"{self.start}:{self.end}"

	def is_overlapped(self, other: Range) -> bool:
		"""
		Checks if the interval overlaps with another interval.

		Notes:
			* The behavior of this method is differs from that of the `Range` class (see example).

		Examples:
			>>> Range(0, 15).is_overlapped(15, 20)
			... False
			>>> InfiniteRange(0, 15).is_overlapped(InfiniteRange(15, 20))
			... True
		"""
		if (self.start is None and self.end is None) or (other.start is None and other.end is None):
			return True

		if self.start is None:
			if other.start is None:
				return True
			else:
				return self.end >= other.start

		if self.end is None:
			if other.end is None:
				return True
			else:
				return self.start <= other.end

		if other.start is None:
			return self.start <= other.end

		if other.end is None:
			return self.end >= other.start

		return max(self.start, other.start) <= min(self.end, other.end)

	def get_overlapped_range(self, other: Range) -> Optional["InfiniteRange"]:
		if self.is_overlapped(other):
			return self.__class__(
				self.get_max_start(self.start, other.start),
				self.get_min_end(self.end, other.end),
			)

		return None

	@staticmethod
	def get_min_end(first, second):
		if first is None and second is None:
			return None
		elif first is None:
			return second
		elif second is None:
			return first

		return min(first, second)

	@staticmethod
	def get_max_start(first, second):
		if first is None and second is None:
			return None
		elif first is None:
			return second
		elif second is None:
			return first

		return max(first, second)

	def concat(self, other: Range) -> Optional[Range]:
		"""
		Combines ranges into one, if possible.

		Args:
			other: Range to concat.

		Returns:
			None if ranges cannot be concatenated.
			New InfinteRange from two ranges.
		"""
		if not self.is_overlapped(other):
			return None

		if (self.start is None and self.end is None) or (other.start is None and other.end is None):
			return self.__class__()

		if self.start is None:
			if other.end is None:
				return self.__class__(None, None)
			else:
				return self.__class__(None, max(self.end, other.end))

		elif self.end is None:
			if other.start is None:
				return self.__class__(None, None)
			else:
				return self.__class__(min(self.start, other.start), None)

		elif other.start is None:
			return self.__class__(None, max(self.end, other.end))

		elif other.end is None:
			return self.__class__(min(self.start, other.start), None)

		return self.__class__(min(self.start, other.start), max(self.end, other.end))

	@classmethod
	def squash(cls, *args):
		"""
		Concatenates passed ranges into longest ranges.

		Returns:
			List of longest independent ranges.

		TODO:
			* The current solution is complex and slow, it may be possible to optimize or/and rework it.

		Warnings:
			* The current solution is slow, use it at your own.
		"""
		ranges = list(args)
		changed = bool(ranges)

		while changed:
			changed = False
			range_to_remove_indexes = []

			for current_range_index, current_range in enumerate(ranges):
				for range_to_concat_index, range_to_concat in enumerate(ranges[current_range_index + 1:]):
					if current_range.is_overlapped(range_to_concat):
						current_range = current_range.concat(range_to_concat)
						changed = True
						range_to_remove_indexes.append(current_range_index + 1 + range_to_concat_index)

				if changed:
					ranges[current_range_index] = current_range
					break

			for index in reversed(range_to_remove_indexes):
				del ranges[index]

		return ranges
