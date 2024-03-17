from .dict import (
	filter_dict, deep_merge, find_field, find_value, normalize_dict,
)

from re import escape
from json import dumps

import pytest


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


class TestFindField:
	@pytest.mark.parametrize(
		"source_dict, candidates, expected_result",
		[
			({'a': 1}, iter('abc'), 'a'),
			({'c': 1}, ('a', 'b', 'c'), 'c'),
			({'c': 1, 'b': 2}, ['a', 'b', 'c'], 'b'),
		],
	)
	def test_find(self, source_dict, candidates, expected_result):
		assert find_field(source_dict, candidates) == expected_result

	@pytest.mark.parametrize(
		"source_dict, candidates",
		[
			({}, []),
			({}, [1]),
			({4: 5}, [1, 2, 3]),
			({'hello': 'world'}, ['world']),
		],
	)
	def test_errors(self, source_dict, candidates):
		with pytest.raises(ValueError, match=f"Can't find any of: {escape(str(candidates))}"):
			find_field(source_dict, candidates)


class TestFindValue:
	@pytest.mark.parametrize(
		"source_dict, candidates, expected_result",
		[
			({'a': 1}, iter('abc'), 1),
			({'c': 1}, ('a', 'b', 'c'), 1),
			({'c': 1, 'b': 2}, ['a', 'b', 'c'], 2),
		],
	)
	def test_find(self, source_dict, candidates, expected_result):
		assert find_value(source_dict, candidates) == expected_result

	@pytest.mark.parametrize(
		"source_dict, candidates",
		[
			({}, []),
			({}, [1]),
			({4: 5}, [1, 2, 3]),
			({'hello': 'world'}, ['world']),
		],
	)
	def test_errors(self, source_dict, candidates):
		with pytest.raises(ValueError, match=f"Can't find any of: {escape(str(candidates))}"):
			find_value(source_dict, candidates)


@pytest.mark.parametrize(
	"source_dict, replacements, allow_original_key, expected_result",
	[
		({}, {}, True, {}),
		({'a': 1}, {'A': ['a1', 'a']}, False, {'A': 1}),
		({'a': 1}, {'a': ['a1']}, True, {'a': 1}),
		({'a': 1, 'b': 2, 'c': 3}, {}, False, {}),
		({'a': 1, 'b': 2, 'c': 3}, {'A': ['a1', 'a'], 'C': ['c1', 'c2', 'c']}, False, {'A': 1, 'C': 3}),
	],
)
def test_normalize_dict(source_dict, replacements, allow_original_key, expected_result):
	assert normalize_dict(source_dict, replacements, allow_original_key) == expected_result
