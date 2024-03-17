def format_long_list(value, prefix=None, max_items=None):
	ret = ''
	if prefix != None:
		ret = prefix

	if max_items is None:
		max_items = len(value)

	leftover = 0
	if len(value) > max_items:
		leftover = len(value) - max_items
		value = value[:max_items]

	ret += ', '.join(value)		# TODO: Add forced conversion to strings
	if leftover > 0:
		ret += f' ...and {leftover} more'

	return ret
