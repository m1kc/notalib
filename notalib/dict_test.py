from .dict import filter_dict, deep_merge, find_field, find_value, normalize_dict

from json import dumps

import pytest


FILTER_DICT_TEST_DATA1 = {
	'Some...': "BODY",
	'once': "told me",
	'the world': "is gonna roll me",
}
FILTER_DICT_TEST_DATA2 = {
	("Some", "body"): ["once", "told me"],
	("The world", "is gonna"): ["roll", "me"],
	("I ain't the", "sharpest tool"): ["in the shed"],
}
NORMALIZE_DICT_REPLACEMENTS = {
	'artist': ['Artist', 'ARTIST'],
	'year': ['Year', 'yr', 'yub'],
}


@pytest.mark.parametrize(
	"dict_, candidates, expected_result",
	[
		({'a': 1, 'b': 2}, ['c', 'd', 'e', 'b', 'f'], 'b'),
		({4: 1}, [1, 2, 3, 4, 'a'], 4),
		({(1, 2): 1, (3, 4): 2}, [1, 2, (3, 4), 1, 2], (3, 4)),
	]
)
def test_find_field(dict_, candidates, expected_result):
	assert find_field(dict_, candidates) == expected_result


def test_find_field_error():
	with pytest.raises(ValueError):
		find_field({}, [])


@pytest.mark.parametrize(
	"dict_, candidates, expected_result",
	[
		({'a': 1, 'b': 2}, ['c', 'd', 'e', 'b', 'f'], 2),
		({4: 1}, [1, 2, 3, 4, 'a'], 1),
		({(1, 2): 1, (3, 4): 2}, [1, 2, (3, 4), 1, 2], 2),
	]
)
def test_find_value(dict_, candidates, expected_result):
	assert find_value(dict_, candidates) == expected_result


@pytest.mark.parametrize(
	"source, replacements, allow_original_key, expected_result",
	[
		({'Artist': 20, 'yr': 23}, NORMALIZE_DICT_REPLACEMENTS, False, {'artist': 20, 'year': 23}),
		({'artist': 15, 'year': 11}, NORMALIZE_DICT_REPLACEMENTS, True, {'artist': 15, 'year': 11}),
	]
)
def test_normalize_dict(source, replacements, allow_original_key, expected_result):
	assert normalize_dict(source, replacements, allow_original_key) == expected_result


@pytest.mark.parametrize(
	"src, leave_only, expected_keys, expected_values",
	[
		(FILTER_DICT_TEST_DATA1, ["Some...", "once"], ("Some...", "once"), ("BODY", "told me")),
		(FILTER_DICT_TEST_DATA1, (), (), ()),
		(FILTER_DICT_TEST_DATA2, [("Some", "body")], (("Some", "body"),), (["once", "told me"],)),
		(FILTER_DICT_TEST_DATA2, (), (), ()),
		({}, ("SOME", "BODY"), (), ()),
		(FILTER_DICT_TEST_DATA2, ("Some...",), (), ()),
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
