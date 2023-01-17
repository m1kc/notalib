from .combinator import Combinator

import pytest


def test_result_getting():
	combinator = Combinator()
	combinator.combine([1, 2, 3, 4])

	assert combinator.result == combinator.get_result()


def test_assertion():
	combinator = Combinator()

	with pytest.raises(AssertionError, match="Combinator cannot combine with empty set"):
		combinator.combine([])
		combinator.combine(())


@pytest.mark.parametrize(
	"src_sets, expected_result",
	[
		(
			[[1, 2], [3, 4], [5, 6]],
			[[1, 3, 5], [1, 3, 6], [1, 4, 5], [1, 4, 6], [2, 3, 5], [2, 3, 6], [2, 4, 5], [2, 4, 6]],
		)
	]
)
def test_combine(src_sets, expected_result):
	combinator = Combinator()

	for s in src_sets:
		combinator.combine(s)

	assert combinator.result == expected_result
