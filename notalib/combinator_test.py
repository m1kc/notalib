from notalib.combinator import Combinator

import pytest


class TestCombinator:
	def test___init__(self):
		assert Combinator.result == []
		assert Combinator().result == []

	def test_combine(self):
		combinator = Combinator()
		combinator.combine([1, 2])
		assert combinator.result == [[1], [2]]
		combinator.combine([3, 4])
		assert combinator.result == [[1, 3], [1, 4], [2, 3], [2, 4]]

	def test_combine_exceptions(self):
		with pytest.raises(Exception, match="Combinator cannot combine with empty set"):
			Combinator().combine([])

	@pytest.mark.parametrize(
		"result, expected_result",
		[
			([], []),
			([1, 2, 3], [1, 2, 3]),
			(['1', '2', '3'], ['1', '2', '3']),
		],
	)
	def test_get_result(self, result, expected_result):
		combinator = Combinator()
		combinator.result = result
		assert combinator.get_result() == expected_result
