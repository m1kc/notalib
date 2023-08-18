from .array import ensure_iterable

import datetime
from typing import Union, NamedTuple, Optional, Collection
from abc import ABC, abstractmethod
from enum import Enum, auto, unique

import arrow


DateLikeObject = Union[datetime.date, datetime.datetime, arrow.Arrow]


class Week(NamedTuple):
	week: int
	year: int

	def __str__(self) -> str:
		return f"{self.week} week of {self.year} year"


@unique
class WeekNumbering(Enum):
	"""
	Contains enumeration of available modes of week extraction.
	"""

	"""
	First day in week is: Monday
	First week number in year is: One
	First week is a week with: The first of Monday
	"""
	NORMAL = auto()

	"""
	First day in week is: Monday
	First week number in year: Zero
	First week is a week with: The first of January
	"""
	MATCH_YEAR = auto()


def parse_month(yyyy_mm):
	a = arrow.get(yyyy_mm, 'YYYY-M')
	return (a.year, a.month)


def parse_date(s, format_or_formats):
	d = None
	for f in ensure_iterable(format_or_formats):
		try:
			d = arrow.get(s, f)
			break
		except:  # should probably narrow to arrow.ParserError
			pass
	if d == None:
		raise ValueError(f"Could not parse date `{s}` with any of the specified formats")
	return d


def normalize_date(
	s: Optional[str],
	input_formats: Collection[str],
	output_format: str,
	allow_empty=True,
) -> Optional[str]:
	"""
	Re-formats a date, parsing it as any of the input_formats and outputting it as output_format.

	This function uses Arrow date formats. See [Arrow docs](https://arrow.readthedocs.io/en/latest/guide.html#supported-tokens) for details.

	Args:
		s: The source date in one of the input_formats to be converted to target format.
		input_formats: Source date representation formats.
		output_format: The format in which the date will be output.
		allow_empty: if true, `None` input will produce `None` output, otherwise a ValueError will be thrown.

	Example:
		>>> normalize_date('12.07.2023', ('D.M.YYYY', 'DD.MM.YYYY'), 'YYYY-MM-DD', False)
		'2023-07-12'

	Returns:
		Converted date string from any of the input formats to the specified output format.
	"""
	if s is None and allow_empty:
		return None

	return parse_date(s, input_formats).format(output_format)


class WeekExtractor(ABC):
	@classmethod
	@abstractmethod
	def extract(cls, date_object: DateLikeObject) -> Week: ...


class MatchYearWeekExtractor(WeekExtractor):
	@classmethod
	def extract(cls, date_object: DateLikeObject) -> Week:
		"""
		Returns week number of specified date with year.
		First week of year is week with monday.
		Range of week numbers: 0..53.
		0 means that week refers to the last week of the previous year.
		"""
		return Week(int(date_object.strftime('%W')), date_object.year)


class NormalWeekExtractor(WeekExtractor):
	@classmethod
	def extract(cls, date_object: DateLikeObject) -> Week:
		"""
		Returns week number of specified date with year.
		First week of year is week with monday.
		Range of week numbers: 1..53.
		"""
		week = MatchYearWeekExtractor.extract(date_object)

		if week.week == 0:
			# Means that the week refers to the last week of the previous year
			week = MatchYearWeekExtractor.extract(datetime.date(date_object.year - 1, 12, 31))

		return week


def get_week(
	date_object: DateLikeObject,
	mode: WeekNumbering = WeekNumbering.NORMAL,
) -> Week:
	"""
	Extracts week from specified date.

	Args:
		date_object: Date like object. It must be compatible with 'datetime.date' object.
		mode: Mode of extraction week number. Available modes see in WeekNumbering.
	"""
	if not isinstance(mode, WeekNumbering):
		raise TypeError(f"The mode {mode} does not belong to the {WeekNumbering.__name__} enumeration")

	if mode == WeekNumbering.NORMAL:
		return NormalWeekExtractor.extract(date_object)
	elif mode == WeekNumbering.MATCH_YEAR:
		return MatchYearWeekExtractor.extract(date_object)

	raise NotImplementedError(f'Extraction week number in mode {mode.name} is not implemented')
