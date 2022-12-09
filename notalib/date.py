from .array import ensure_iterable
from .deprecated import deprecated

import datetime
from typing import Union, NamedTuple
from abc import ABC, abstractmethod
from enum import Enum, auto, unique

import arrow


DateLikeObject = Union[datetime.date, datetime.datetime, arrow.Arrow]


class YearWeekNumber(NamedTuple):
	week: int
	year: int

	def __str__(self) -> str:
		return f"{self.week} week of {self.year} year"


@unique
class YearWeekNumberExtractionMode(Enum):
	"""
	Contains enumeration of available modes of year week number extraction.
	"""

	"""
	First day in week is: Monday
	First week number in year is: Zero
	First week is a week with: The first of January
	"""
	MODE_NORMAL = auto()

	"""
	First day in week is: Monday
	First week number in year: One
	First week is a week with: The first of Monday
	"""
	MODE_MATCH_YEAR = auto()


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


def normalize_date(s, input_formats, output_format, allow_empty=True):
	if s == None and allow_empty:
		return None
	return parse_date(s, input_formats).format(output_format)


class YearWeekNumberExtractor(ABC):
	@classmethod
	@abstractmethod
	def extract(cls, date_object: DateLikeObject) -> YearWeekNumber: ...


class YearWeekNumberExtractorNormalMode(YearWeekNumberExtractor):
	@classmethod
	def extract(cls, date_object: DateLikeObject) -> YearWeekNumber:
		"""
		Returns week number of specified date with year.
		First week of year is week with monday.
		Range of week numbers: 0..53.
		0 means that week refers to the last week of the previous year.
		"""
		return YearWeekNumber(int(date_object.strftime('%W')), date_object.year)


class YearWeekNumberExtractorMatchYearMode(YearWeekNumberExtractor):
	@classmethod
	def extract(cls, date_object: DateLikeObject) -> YearWeekNumber:
		"""
		Returns week number of specified date with year.
		First week of year is week with monday.
		Range of week numbers: 1..53.
		"""
		year_week_number = YearWeekNumberExtractorNormalMode.extract(date_object)

		if year_week_number.week == 0:
			# Means that the week refers to the last week of the previous year
			year_week_number = YearWeekNumberExtractorNormalMode.extract(datetime.date(date_object.year - 1, 12, 31))

		return year_week_number


def extract_year_week_number(
	date_object: DateLikeObject,
	mode: YearWeekNumberExtractionMode = YearWeekNumberExtractionMode.MODE_NORMAL,
) -> YearWeekNumber:
	"""
	Extracts year week number from specified date.

	Args:
		date_object: Date like object. It must be compatible with 'datetime.date' object.
		mode: Mode of extraction week number. Available modes see in YearWeekNumberExtractionMode.
	"""
	if not isinstance(mode, YearWeekNumberExtractionMode):
		raise TypeError(f"The mode {mode} does not belong to the {YearWeekNumberExtractionMode.__name__} enumeration")

	if mode == YearWeekNumberExtractionMode.MODE_NORMAL:
		return YearWeekNumberExtractorNormalMode.extract(date_object)
	elif mode == YearWeekNumberExtractionMode.MODE_MATCH_YEAR:
		return YearWeekNumberExtractorMatchYearMode.extract(date_object)

	raise NotImplementedError(f'Extraction week number in mode {mode.name} is not implemented')


@deprecated(
	reason=(
		f"Starting from version ^1.3.3, the function {__name__}.get_week_number is deprecated. "
		f"Use {__name__}.{extract_year_week_number.__name__} instead of this function."
	)
)
def get_week_number(date: arrow.Arrow) -> int:
	"""
	Returns the number of the week by date

	Notes:
		strftime method with parameter '%W' returns week number in range 0...53 where is a monday is a first day of week.

	01.01.2022 is a first week of year, but method returns 0. To result in a human-readable format, 1 is added.
	"""
	return int(date.strftime('%W')) + 1
