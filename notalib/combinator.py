from typing import Sequence


class Combinator:
	"""
	Combines multiple data sets into a set of their combinations.

	Examples:
		>>> combinator = Combinator()
		>>> combinator.combine([1, 2])
		>>> combinator.result
		[[1], [2]]
		>>> combinator.combine([3, 4])
		>>> combinator.result
		[[1, 3], [1, 4], [2, 3], [2, 4]]
		>>> combinator.combine([5, 6])
		>>> combinator.result
		[[1, 3, 5], [1, 3, 6], [1, 4, 5], [1, 4, 6], [2, 3, 5], [2, 3, 6], [2, 4, 5], [2, 4, 6]]
	"""
	_result = []

	def __init__(self):
		self._result = []

	def combine(self, new_set: Sequence) -> None:
		"""
		Adds new set to combination result.

		Args:
			new_set: Values to be added to the combination.

		Returns: None

		Raises:
			AssertionError: When new set has an empty length.
		"""
		assert len(new_set) > 0, "Combinator cannot combine with empty set"

		if len(self._result) == 0:
			for i in new_set:
				self._result += [[i]]
		else:
			new_result = []

			for i in self._result:
				for k in new_set:
					new_result += [i + [k]]

			self._result = new_result

	@property
	def result(self) -> list:
		return self._result

	def get_result(self) -> list:
		return self.result
