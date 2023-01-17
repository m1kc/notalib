from .date import Week, get_week, WeekNumbering, parse_month, parse_date, normalize_date

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


@pytest.mark.parametrize(
	"yyyy_mm, expected_result",
	[
		('2022-1', (2022, 1)),
		('2024-12', (2024, 12))
	]
)
def test_parse_month(yyyy_mm, expected_result):
	assert parse_month(yyyy_mm) == expected_result


@pytest.mark.parametrize(
	"date, format_or_formats",
	[
		('', 'YYYY-MM'),
		('', ['YYYY', 'MM']),
	]
)
def test_parse_date_errors(date, format_or_formats):
	with pytest.raises(ValueError):
		parse_date(date, format_or_formats)


@pytest.mark.parametrize(
	"date, format_or_formats, expected_result",
	[
		('2022-12-11', 'YYYY-MM-DD', arrow_get(2022, 12, 11)),
		('2022-12', ['YYYY-MM-DD', 'YYYY-MM'], arrow_get(2022, 12, 1)),
	]
)
def test_parse_date(date, format_or_formats, expected_result):
	assert parse_date(date, format_or_formats) == expected_result


@pytest.mark.parametrize(
	"date, input_formats, output_format, allow_empty, expected_result",
	[
		('2022-12-12', 'YYYY-MM-DD', 'YYYY-MM', False, '2022-12'),
		('2023-01', ['YYYY-MM-DD', 'YYYY-MM'], 'YYYY-MM-DD', False, '2023-01-01'),
		(None, [], '', True, None)
	]
)
def test_normalize_date(date, input_formats, output_format, allow_empty, expected_result):
	assert normalize_date(date, input_formats, output_format, allow_empty) == expected_result


@pytest.mark.parametrize(
	"date, mode, expected_week_number",
	GET_WEEK_TEST_DATA,
)
def test_get_week(date, mode, expected_week_number):
	assert get_week(date, mode) == expected_week_number
