from typing import Sequence, Hashable, Optional, Iterable, Any, Dict, TypeVar


DictKey = TypeVar('DictKey', bound=Hashable)


def find_field(d: dict, candidates: Iterable[Hashable]) -> Hashable:
	"""
	Finds the first available key in the specified dictionary.

	Args:
		d: Dictionary in which to search for keys.
		candidates: Possible keys.

	Raises:
		ValueError: If key not found.
	"""
	for c in candidates:
		if c in d:
			return c

	raise ValueError(f"Can't find any of: {candidates}")


def find_value(d: dict, candidates: Iterable[Hashable]) -> Any:
	"""
	Finds the first available key in the specified dictionary and returns value by it.

	Args:
		d: Dictionary in which to search for keys.
		candidates: Possible keys.
	"""
	field_name = find_field(d, candidates)
	return d[field_name]


def normalize_dict(
	source: Dict[DictKey, Any],
	replacements: Dict[DictKey, Sequence[DictKey]],
	allow_original_key=True,
) -> dict:
	"""
	Normalizes the source dictionary keys using the specified substitutions.

	Typically used to normalize a dataset where the same info can be listed
	under different names.

	Args:
		source: The dictionary in which to normalize the keys.
		replacements: Possible keys with replacements.
		allow_original_key: Flag for using a key in replacements as a key in a source dictionary.

	Returns:
		A new dict where all keys are guaranteed to be reference keys with values taken from any of replacement
		keys.

	Examples:
		>>> replacements = {
		>>> 	"artist": ["Artist", "ARTIST"],
		>>> 	"year": ["Year", "yr", "yob"],
		>>> }
		>>> source = {
		>>> 	'ARTIST': 'Ivanov Ivan',
		>>> 	'yr': 2012,
		>>> }
		>>> normalize_dict(source, replacements)
		{
			'artist': 'Ivanov Ivan',
			'year': 2012,
		}
	"""
	ret = {}

	for key in replacements:
		candidates = replacements[key]

		if allow_original_key:
			candidates = list(candidates) + [key]

		value = find_value(source, candidates)
		ret[key] = value

	return ret


def filter_dict(src: Dict[DictKey, Any], keys_to_filter: Sequence[DictKey]) -> dict:
	"""
	Filters dictionary by keys_to_filter set.

	Args:
		src: Source dictionary.
		keys_to_filter: Set of keys that should be in the final dictionary.

	Returns:
		New dictionary with data from filtered source dict.
	"""
	return {key: value for key, value in src.items() if key in keys_to_filter}


def deep_merge(orig: dict, other: dict, overwrite: bool = False, __path: Optional[list] = None) -> dict:
	"""
	Merges two dictionaries.

	Args:
		orig: The original dictionary that will be changed.
		other: Another dictionary whose values will be added to the original one.
		overwrite: Flag for overwriting values.
			If True, the values in the original dictionary will be overwritten if the keys match.
			If False, an error will be raised if the values match by keys.
		__path: Contains the debug path to the key that an error occurred when merging.

	Returns:
		Modified original dictionary.

	Notes:
		The original dictionary will be changed.
			Use copy.deepcopy to create a deep copy of the original dictionary and avoid modifying it.

	Raises:
		Exception: If, when merging dictionaries, there was a match of keys and a mismatch of values.

	Source: https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries/7205107#7205107
	"""
	__path = __path or []

	for key in other:
		if key in orig:
			if isinstance(orig[key], dict) and isinstance(other[key], dict):
				deep_merge(orig[key], other[key], overwrite, __path + [str(key)])

			elif orig[key] != other[key]:
				if overwrite:
					orig[key] = other[key]
				else:
					raise Exception('Conflict at %s' % '.'.join(__path + [str(key)]))
		else:
			orig[key] = other[key]

	return orig
