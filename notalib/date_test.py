from .date import Week, get_week, WeekNumbering, normalize_date, parse_date

from unittest.mock import patch
from enum import Enum

import pytest
from arrow import get as arrow_get


GET_WEEK_TEST_DATA = [
	(arrow_get(2018, 12, 30), WeekNumbering.MATCH_YEAR, Week(52, 2018)),
	(arrow_get(2018, 12, 31), WeekNumbering.MATCH_YEAR, Week(53, 2018)),
	(arrow_get(2019, 1, 1), WeekNumbering.MATCH_YEAR, Week(0, 2019)),
	(arrow_get(2019, 1, 7), WeekNumbering.MATCH_YEAR, Week(1, 2019)),
	(arrow_get(2021, 12, 31), WeekNumbering.MATCH_YEAR, Week(52, 2021)),
	(arrow_get(2022, 1, 1), WeekNumbering.MATCH_YEAR, Week(0, 2022)),
	(arrow_get(2022, 12, 31), WeekNumbering.MATCH_YEAR, Week(52, 2022)),
	(arrow_get(2023, 1, 1), WeekNumbering.MATCH_YEAR, Week(0, 2023)),
	(arrow_get(2023, 1, 2), WeekNumbering.MATCH_YEAR, Week(1, 2023)),
	(arrow_get(2023, 1, 3), WeekNumbering.MATCH_YEAR, Week(1, 2023)),
	(arrow_get(2023, 12, 31), WeekNumbering.MATCH_YEAR, Week(52, 2023)),
	(arrow_get(2024, 1, 1), WeekNumbering.MATCH_YEAR, Week(1, 2024)),
	(arrow_get(2024, 1, 8), WeekNumbering.MATCH_YEAR, Week(2, 2024)),
	(arrow_get(2018, 12, 30), WeekNumbering.NORMAL, Week(52, 2018)),
	(arrow_get(2018, 12, 31), WeekNumbering.NORMAL, Week(53, 2018)),
	(arrow_get(2019, 1, 1), WeekNumbering.NORMAL, Week(53, 2018)),
	(arrow_get(2019, 1, 7), WeekNumbering.NORMAL, Week(1, 2019)),
	(arrow_get(2021, 12, 31), WeekNumbering.NORMAL, Week(52, 2021)),
	(arrow_get(2022, 1, 1), WeekNumbering.NORMAL, Week(52, 2021)),
	(arrow_get(2022, 12, 31), WeekNumbering.NORMAL, Week(52, 2022)),
	(arrow_get(2023, 1, 1), WeekNumbering.NORMAL, Week(52, 2022)),
	(arrow_get(2023, 1, 2), WeekNumbering.NORMAL, Week(1, 2023)),
	(arrow_get(2023, 1, 3), WeekNumbering.NORMAL, Week(1, 2023)),
	(arrow_get(2023, 12, 31), WeekNumbering.NORMAL, Week(52, 2023)),
	(arrow_get(2024, 1, 1), WeekNumbering.NORMAL, Week(1, 2024)),
	(arrow_get(2024, 1, 8), WeekNumbering.NORMAL, Week(2, 2024)),
]


class TestGetWeek:
	@pytest.mark.parametrize(
		"date, mode, expected_week_number",
		GET_WEEK_TEST_DATA,
	)
	def test_get_week(self, date, mode, expected_week_number):
		assert get_week(date, mode) == expected_week_number

	def test_errors(self):
		with pytest.raises(TypeError):
			get_week(arrow_get(2023, 1, 1, 11, 1), None)		# type: ignore

		FakeWeekNumbering = Enum('FakeWeekNumbering', {'NORMAL': 1, 'MATCH_YEAR': 2, 'UNKNOWN': 99})

		with patch('notalib.date.WeekNumbering', new=FakeWeekNumbering):
			with pytest.raises(NotImplementedError, match="Extraction week number in mode UNKNOWN is not implemented"):
				get_week(arrow_get(2023, 1, 1, 11, 1), getattr(FakeWeekNumbering, 'UNKNOWN'))


@pytest.mark.parametrize(
	"date, input_formats, output_format, allow_empty, expected_result",
	[
		(None, (), '', True, None),
		('3.8.2023', ('D.M.YYYY',), 'YYYY-MM-DD', False, '2023-08-03'),
		('03.08.2023', ('D.M.YYYY', 'DD.MM.YYYY'), 'YYYYMMDD', True, '20230803'),
	],
)
def test_normalize_date(date, input_formats, output_format, allow_empty, expected_result):
	assert normalize_date(date, input_formats, output_format, allow_empty) == expected_result


class TestWeek:
	@pytest.mark.parametrize(
		"week, expected_string",
		[
			(Week(0, 0), "0 week of 0 year"),
			(Week(0, 2023), "0 week of 2023 year"),
			(Week(16, 0), "16 week of 0 year"),
			(Week(16, 2023), "16 week of 2023 year"),
			(Week(-2023, -16), "-2023 week of -16 year"),
		],
	)
	def test___str__(self, week: Week, expected_string: str):
		assert week.__str__() == expected_string


class TestParseDate:
	@pytest.mark.parametrize(
		"date_string, date_format, expected_result",
	[
		("2023-01-01", "YYYY-MM-DD", arrow_get(2023, 1, 1)),
		("01-01-2023", "DD-MM-YYYY", arrow_get(2023, 1, 1)),
		("2023/01/01", "YYYY/MM/DD", arrow_get(2023, 1, 1)),
		("2023-01-01", ["YYYY-MM-DD", "MM/DD/YYYY"], arrow_get(2023, 1, 1)),
		("01/01/2023", ["DD/MM/YYYY", "MM/DD/YYYY"], arrow_get(2023, 1, 1)),
		("2023-01-01 12:00", "YYYY-MM-DD HH:mm", arrow_get(2023, 1, 1, 12, 0)),
		("01-01-2023 23:59", "DD-MM-YYYY HH:mm", arrow_get(2023, 1, 1, 23, 59)),
		("2023/01/01 6:00 AM", "YYYY/MM/DD h:mm A", arrow_get(2023, 1, 1, 6, 0)),
	])
	def test_parse(self, date_string, date_format, expected_result):
		assert parse_date(date_string, date_format) == arrow_get(date_string, date_format)

	@pytest.mark.parametrize(
		"date_string, date_format",
	[
		("2023-01-01", "MM/DD/YYYY"),
		("01/01/2023", "YYYY-MM-DD"),
		("2023-01-01 12:00", "MM/DD/YYYY HH:mm"),
		("01/01/2023 11:59 PM", "YYYY-MM-DD HH:mm A"),
		("2023-01-01", ["MM/DD/YYYY", "DD/MM/YYYY"]),
		("01/01/2023", ["YYYY/DD/MM", "MM-DD-YYYY"]),
		("2023-01-01 12:00", ["MM/DD/YYYY h:mm A", "DD/MM/YYYY HH:mm A"]),
		("01/01/2023 11:59 PM", ["YYYY/DD/MM HH:mm", "MM-DD-YYYY h:mm A"]),
		("01/01/2023", []),
		("01/01/2023", None),
		(12345, "YYYY-MM-DD"),
		(None, "MM/DD/YYYY"),
	])
	def test_error(self, date_string, date_format):
		with pytest.raises(ValueError):
			parse_date(date_string, date_format)
