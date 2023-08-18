from .date import Week, get_week, WeekNumbering, normalize_date

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
	"date, mode, expected_week_number",
	GET_WEEK_TEST_DATA,
)
def test_get_week(date, mode, expected_week_number):
	assert get_week(date, mode) == expected_week_number


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
