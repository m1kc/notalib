from .date import get_week_number, YearWeekNumber, extract_year_week_number, YearWeekNumberExtractionMode

import pytest
from arrow import get as arrow_get


GET_WEEK_NUMBER_TEST_DATA = [
	(arrow_get(2018, 12, 30), 53),
	(arrow_get(2018, 12, 31), 54),
	(arrow_get(2019, 1, 1), 1),
	(arrow_get(2019, 1, 7), 2),
	(arrow_get(2021, 12, 31), 53),
	(arrow_get(2022, 1, 1), 1),
	(arrow_get(2022, 12, 31), 53),
	(arrow_get(2023, 1, 1), 1),
	(arrow_get(2023, 1, 2), 2),
	(arrow_get(2023, 1, 3), 2),
	(arrow_get(2023, 12, 31), 53),
	(arrow_get(2024, 1, 1), 2),
	(arrow_get(2024, 1, 8), 3),
]

EXTRACT_YEAR_WEEK_NUMBER_TEST_DATA = [
	(arrow_get(2018, 12, 30), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(52, 2018)),
	(arrow_get(2018, 12, 31), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(53, 2018)),
	(arrow_get(2019, 1, 1), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(0, 2019)),
	(arrow_get(2019, 1, 7), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(1, 2019)),
	(arrow_get(2021, 12, 31), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(52, 2021)),
	(arrow_get(2022, 1, 1), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(0, 2022)),
	(arrow_get(2022, 12, 31), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(52, 2022)),
	(arrow_get(2023, 1, 1), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(0, 2023)),
	(arrow_get(2023, 1, 2), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(1, 2023)),
	(arrow_get(2023, 1, 3), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(1, 2023)),
	(arrow_get(2023, 12, 31), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(52, 2023)),
	(arrow_get(2024, 1, 1), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(1, 2024)),
	(arrow_get(2024, 1, 8), YearWeekNumberExtractionMode.MODE_NORMAL, YearWeekNumber(2, 2024)),
	(arrow_get(2018, 12, 30), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(52, 2018)),
	(arrow_get(2018, 12, 31), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(53, 2018)),
	(arrow_get(2019, 1, 1), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(53, 2018)),
	(arrow_get(2019, 1, 7), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(1, 2019)),
	(arrow_get(2021, 12, 31), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(52, 2021)),
	(arrow_get(2022, 1, 1), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(52, 2021)),
	(arrow_get(2022, 12, 31), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(52, 2022)),
	(arrow_get(2023, 1, 1), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(52, 2022)),
	(arrow_get(2023, 1, 2), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(1, 2023)),
	(arrow_get(2023, 1, 3), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(1, 2023)),
	(arrow_get(2023, 12, 31), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(52, 2023)),
	(arrow_get(2024, 1, 1), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(1, 2024)),
	(arrow_get(2024, 1, 8), YearWeekNumberExtractionMode.MODE_MATCH_YEAR, YearWeekNumber(2, 2024)),
]


@pytest.mark.parametrize(
	"date, expected_week_number",
	GET_WEEK_NUMBER_TEST_DATA,
)
def test_get_week_number(date, expected_week_number):
	assert get_week_number(date) == expected_week_number


@pytest.mark.parametrize(
	"date, mode, expected_week_number",
	EXTRACT_YEAR_WEEK_NUMBER_TEST_DATA,
)
def test_extract_year_week_number(date, mode, expected_week_number):
	assert extract_year_week_number(date, mode) == expected_week_number
