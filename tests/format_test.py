from notalib.format import format_long_seq

import pytest


@pytest.mark.parametrize(
	"seq, prefix, max_items, expected_result",
	[
		(['1', '2', '3'], None, 3, "1, 2, 3"),
		(['1', '2', '3'], None, 1, "1 ...and 2 more"),
		(['1', '2', '3'], None, 1, "1 ...and 2 more"),
		([], None, 0, ""),
		(['1', '2', '3'], None, 0, " ...and 3 more"),
		(['1'], 'Prefix: ', 1, "Prefix: 1"),
		(['1'], 'Prefix: ', 0, "Prefix:  ...and 1 more"),
	]
)
def test_format_long_seq(seq, prefix, max_items, expected_result):
	assert format_long_seq(seq, prefix, max_items) == expected_result
