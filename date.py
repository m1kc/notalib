from .array import ensure_iterable

import arrow


def parse_month(yyyy_mm):
	a = arrow.get(yyyy_mm, 'YYYY-M')
	return (a.year, a.month)


def parse_date(s, format_or_formats):
	d = None
	for f in ensure_iterable(format_or_formats):
		try:
			d = arrow.get(s, f)
			break
		except:
			pass
	if d == None:
		raise ValueError(f"Could not parse date `{s}` with any of the specified formats")
	return d

def normalize_date(s, input_formats, output_format, allow_empty=True):
	if s == None and allow_empty:
		return None
	return parse_date(s, input_formats).format(output_format)
