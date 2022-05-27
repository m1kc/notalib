from .pandasplus import replace_null_objects

from pytest import mark
from arrow import get as arrow_get
from pandas import DataFrame, NaT, NA


SOURCE_DATAFRAME = DataFrame(
	{
		"dates": [arrow_get("2021-09-07").date(), arrow_get("2007-01-01").date(), NaT],
		"strings": ["Some Data", None, NA],
		"numbers": [1511, NA, 0],
	}
)


@mark.parametrize(
	"src, new_value, expected_proc",
	[
		(
			SOURCE_DATAFRAME,
			None,
			{
				"dates": [arrow_get("2021-09-07").date(), arrow_get("2007-01-01").date(), None],
				"strings": ["Some Data", None, None],
				"numbers": [1511, None, 0],
			},
		),
		(
			SOURCE_DATAFRAME,
			"notalib but a conservative",
			{
				"dates": [arrow_get("2021-09-07").date(), arrow_get("2007-01-01").date(), "notalib but a conservative"],
				"strings": ["Some Data", "notalib but a conservative", "notalib but a conservative"],
				"numbers": [1511, "notalib but a conservative", 0],
			},
		),
		(
			SOURCE_DATAFRAME,
			1998,
			{
				"dates": [arrow_get("2021-09-07").date(), arrow_get("2007-01-01").date(), 1998],
				"strings": ["Some Data", 1998, 1998],
				"numbers": [1511, 1998, 0],
			},
		),
		(
			DataFrame(),
			None,
			{},
		)
	]
)
def test_replace_null_objects(src, new_value, expected_proc):
	proc = replace_null_objects(src, new_value)

	if not src.empty:
		assert proc.columns.tolist() == list(expected_proc.keys())

		assert proc.dates.tolist() == expected_proc['dates']
		assert proc.strings.tolist() == expected_proc['strings']
		assert proc.numbers.tolist() == expected_proc['numbers']

	else:
		assert proc.empty
