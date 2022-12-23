from typing import Sequence, Hashable, Optional


def find_field(d, candidates):
	"""
	Given a dict and a list of possible keys, find the first key
	which is included into this dict. Throws ValueError if not found.
	"""
	for c in candidates:
		if c in d:
			return c
	raise ValueError(f"Can't find any of: {candidates}")


def find_value(d, candidates):
	"""
	Given a dict and a list of possible keys, find the first key
	which is included into this dict and return its value.
	Throws ValueError if not found.
	"""
	fieldname = find_field(d, candidates)
	return d[fieldname]


def normalize_dict(source, replacements, allow_original_key=True):
	"""
	Given a dict and a map: reference key -> [] possible replacements,
	return a new dict where all keys are guaranteed to be reference keys
	with values taken from any of replacement keys.

	Typically used to normalize a dataset where the same info can be listed
	under different names.

	Example map:
	{
		"artist": ["Artist", "ARTIST"],
		"year": ["Year", "yr", "yob"],
	}
	"""
	ret = {}
	for key in replacements:
		candidates = replacements[key]
		if allow_original_key:
			candidates += (key,)
		value = find_value(source, candidates)
		ret[key] = value
	return ret


def filter_dict(src: dict, keys_to_filter: Sequence[Hashable]) -> dict:
	"""
	Filters dictionary by keys_to_filter set.

	Args:
		src: Source dictionary.
		keys_to_filter: Set of keys that should be in the final dictionary.

	Returns:
		Filtered source dictionary.
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
