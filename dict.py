def find_field(d, candidates):
	for c in candidates:
		if c in d:
			return c
	raise ValueError(f"Can't find any of: {candidates}")

def find_value(d, candidates):
	fieldname = find_field(d, candidates)
	return d[fieldname]

def normalize_dict(source, replacements, allow_original_key=True):
	ret = {}
	for key in replacements:
		candidates = replacements[key]
		if allow_original_key:
			candidates += (key,)
		value = find_value(source, candidates)
		ret[key] = value
	return ret
