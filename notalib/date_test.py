from .date import Week, get_week, WeekExtractionMode

import pytest
from arrow import get as arrow_get


EXTRACT_YEAR_WEEK_NUMBER_TEST_DATA = [
	(arrow_get(2018, 12, 30), WeekExtractionMode.MODE_MATCH_YEAR, Week(52, 2018)),
	(arrow_get(2018, 12, 31), WeekExtractionMode.MODE_MATCH_YEAR, Week(53, 2018)),
	(arrow_get(2019, 1, 1), WeekExtractionMode.MODE_MATCH_YEAR, Week(0, 2019)),
	(arrow_get(2019, 1, 7), WeekExtractionMode.MODE_MATCH_YEAR, Week(1, 2019)),
	(arrow_get(2021, 12, 31), WeekExtractionMode.MODE_MATCH_YEAR, Week(52, 2021)),
	(arrow_get(2022, 1, 1), WeekExtractionMode.MODE_MATCH_YEAR, Week(0, 2022)),
	(arrow_get(2022, 12, 31), WeekExtractionMode.MODE_MATCH_YEAR, Week(52, 2022)),
	(arrow_get(2023, 1, 1), WeekExtractionMode.MODE_MATCH_YEAR, Week(0, 2023)),
	(arrow_get(2023, 1, 2), WeekExtractionMode.MODE_MATCH_YEAR, Week(1, 2023)),
	(arrow_get(2023, 1, 3), WeekExtractionMode.MODE_MATCH_YEAR, Week(1, 2023)),
	(arrow_get(2023, 12, 31), WeekExtractionMode.MODE_MATCH_YEAR, Week(52, 2023)),
	(arrow_get(2024, 1, 1), WeekExtractionMode.MODE_MATCH_YEAR, Week(1, 2024)),
	(arrow_get(2024, 1, 8), WeekExtractionMode.MODE_MATCH_YEAR, Week(2, 2024)),
	(arrow_get(2018, 12, 30), WeekExtractionMode.MODE_NORMAL, Week(52, 2018)),
	(arrow_get(2018, 12, 31), WeekExtractionMode.MODE_NORMAL, Week(53, 2018)),
	(arrow_get(2019, 1, 1), WeekExtractionMode.MODE_NORMAL, Week(53, 2018)),
	(arrow_get(2019, 1, 7), WeekExtractionMode.MODE_NORMAL, Week(1, 2019)),
	(arrow_get(2021, 12, 31), WeekExtractionMode.MODE_NORMAL, Week(52, 2021)),
	(arrow_get(2022, 1, 1), WeekExtractionMode.MODE_NORMAL, Week(52, 2021)),
	(arrow_get(2022, 12, 31), WeekExtractionMode.MODE_NORMAL, Week(52, 2022)),
	(arrow_get(2023, 1, 1), WeekExtractionMode.MODE_NORMAL, Week(52, 2022)),
	(arrow_get(2023, 1, 2), WeekExtractionMode.MODE_NORMAL, Week(1, 2023)),
	(arrow_get(2023, 1, 3), WeekExtractionMode.MODE_NORMAL, Week(1, 2023)),
	(arrow_get(2023, 12, 31), WeekExtractionMode.MODE_NORMAL, Week(52, 2023)),
	(arrow_get(2024, 1, 1), WeekExtractionMode.MODE_NORMAL, Week(1, 2024)),
	(arrow_get(2024, 1, 8), WeekExtractionMode.MODE_NORMAL, Week(2, 2024)),
]


@pytest.mark.parametrize(
	"date, mode, expected_week_number",
	EXTRACT_YEAR_WEEK_NUMBER_TEST_DATA,
)
def test_get_week(date, mode, expected_week_number):
	assert get_week(date, mode) == expected_week_number
