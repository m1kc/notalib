from notalib.format import format_long_list

import pytest


@pytest.mark.parametrize(
	"value, prefix, max_items, expected_result",
	[
		([], None, None, ""),
		([], "prefix", None, "prefix"),
		([], "prefix", 10, "prefix"),
		(['1', '2', '3'], "prefix", 0, "prefix ...and 3 more"),
		(['1', '2', '3'], "prefix", 10, "prefix1, 2, 3"),
		(['1', '2', '3'], "prefix", 2, "prefix1, 2 ...and 1 more"),

		# FIXME: This behavior is incorrect
		(['1', '2', '3'], "prefix", -2, "prefix1 ...and 5 more"),
	],
)
def test_format_long_list(value, prefix, max_items, expected_result):
	assert format_long_list(value, prefix, max_items) == expected_result
