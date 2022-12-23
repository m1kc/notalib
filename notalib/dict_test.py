from .dict import filter_dict, deep_merge

import pytest
from json import dumps


FIRST_SRC_DICT = {
	'Some...': "BODY",
	'once': "told me",
	'the world': "is gonna roll me",
}
SECOND_SRC_DICT = {
	("Some", "body"): ["once", "told me"],
	("The world", "is gonna"): ["roll", "me"],
	("I ain't the", "sharpest tool"): ["in the shed"],
}


@pytest.mark.parametrize(
	"src, leave_only, expected_keys, expected_values",
	[
		(FIRST_SRC_DICT, ["Some...", "once"], ("Some...", "once"), ("BODY", "told me")),
		(FIRST_SRC_DICT, (), (), ()),
		(SECOND_SRC_DICT, [("Some", "body")], (("Some", "body"), ), (["once", "told me"], )),
		(SECOND_SRC_DICT, (), (), ()),
		({}, ("SOME", "BODY"), (), ()),
		(SECOND_SRC_DICT, ("Some...", ), (), ()),
		([], ("SOME", "BODY"), None, None)
	]
)
def test_filter_dict(src, leave_only, expected_keys, expected_values):
	if isinstance(src, dict):
		filtered_dict = filter_dict(src, leave_only)

		assert tuple(filtered_dict.keys()) == expected_keys
		assert tuple(filtered_dict.values()) == expected_values

	else:
		with pytest.raises(AttributeError, match=".* object has no attribute 'items'"):
			filter_dict(src, leave_only)


@pytest.mark.parametrize(
	"orig, other, overwrite, expected_result",
	[
		({'a': 1}, {'b': 2}, False, {'a': 1, 'b': 2}),
		({'a': 1}, {'a': 1}, False, {'a': 1}),
		({'a': 1}, {'a': 2}, True, {'a': 2}),
		({'a': {'a': 5}}, {'a': {'b': 12}}, False, {'a': {'a': 5, 'b': 12}}),
		({'a': {'a': 5}}, {'a': {'a': 12}}, True, {'a': {'a': 12}}),
		(
			{'h': {'e': {'l': {'l': 'o'}}}},
			{'h': {'e': {'l': {'l': {'o': '!'}}}}},
			True,
			{'h': {'e': {'l': {'l': {'o': '!'}}}}},
		),
	]
)
def test_deep_merge(orig, other, overwrite, expected_result):
	assert dumps(deep_merge(orig, other, overwrite), sort_keys=True) == dumps(expected_result, sort_keys=True)


@pytest.mark.parametrize(
	"orig, other, conflict_path",
	[
		({'a': 1}, {'a': 2}, 'a'),
		({'a': {'a': 5}}, {'a': {'a': 12}}, 'a.a'),
	]
)
def test_deep_merge_raise_error(orig, other, conflict_path):
	with pytest.raises(Exception, match=f"Conflict at {conflict_path}"):
		deep_merge(orig, other)
