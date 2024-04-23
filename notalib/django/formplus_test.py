from .formplus import MonthArrayField, MonthField, ChoiceWithDefault, IntegerArrayField, StringArrayField

from typing import Tuple
from datetime import date

from django.core.exceptions import ValidationError
import pytest
from hypothesis import given
from hypothesis.strategies import lists, dates



class TestMonthArrayField:
	def test___init__(self):
		field = MonthArrayField()
		assert field.sep == "|"

		field = MonthArrayField(sep=";", required=True, help_text="Help text")
		assert field.sep == ";"
		assert field.required and field.help_text == "Help text"

	@pytest.mark.parametrize(
		"sep, value, expected_result",
		[
			("|", None, None),
			("|", "2019-01", [(2019, 1)]),
			("|", "1999-02", [(1999, 2)]),
			("|", "2019-01|2019-02|1917-10", [(2019, 1), (2019, 2), (1917, 10)]),
			(";", "2019-01;2019-02;1917-10", [(2019, 1), (2019, 2), (1917, 10)]),
		],
	)
	def test_clean_correctness(self, sep, value, expected_result):
		field = MonthArrayField(sep=sep)
		assert field.clean(value) == expected_result

	@pytest.mark.parametrize(
		"sep, value",
		[
			("|", "2678"),
			("|", "-01"),
			("|", "2019-01|672643787878"),
			("|", "2019-01|2099-01||||||||||||||||	  "),
			("|", "2019-13"),
			(";", "2019-01|2019-02|1917-10"),
		],
	)
	def test_clean_exceptions(self, sep, value):
		field = MonthArrayField(sep=sep)

		with pytest.raises(ValidationError):
			field.clean(value)


	# Hypothesis can generate a year that is less than the minimum allowed year in Arrow
	@given(lists(dates(min_value=date(1000, 1, 1)), min_size=1))
	def test_clean_random(self, source):
		field = MonthArrayField()
		result = field.clean('|'.join([f"{i.year}-{i.month}" for i in source]))

		for i in range(0, len(result)):
			assert result[i] == (source[i].year, source[i].month)


class TestMonthField:
	@pytest.mark.parametrize(
		"month, expected_result",
		[
			("2023-1", (2023, 1)),
			("2023-2", (2023, 2)),
			("2023-3", (2023, 3)),
			("2023-4", (2023, 4)),
			("2023-5", (2023, 5)),
			("2023-6", (2023, 6)),
			("2023-7", (2023, 7)),
			("2023-8", (2023, 8)),
			("2023-9", (2023, 9)),
			("2023-10", (2023, 10)),
			("2023-11", (2023, 11)),
			("2023-12", (2023, 12)),
		],
	)
	def test_clean_correctness(self, month: str, expected_result: Tuple[int, int]):
		field = MonthField()
		assert field.clean(month) == expected_result

	@pytest.mark.parametrize(
		"month",
		[
			("23-1", ),
			("2023-01", ),
			("01-2023", ),
			("1-2023", ),
		],
	)
	def test_clean_exceptions(self, month: str):
		field = MonthField()

		with pytest.raises(ValidationError) as excinfo:
			field.clean(month)

		assert excinfo.value.message == "Not a valid month (expected YYYY-MM)"


class TestChoiceWithDefault:
	def test___init__(self):
		with pytest.raises(KeyError):
			ChoiceWithDefault()

		field = ChoiceWithDefault(default="default", required=True, help_text="Help text")

		assert field.default_value == "default"
		assert field.required and field.help_text == "Help text"

	def test_clean_correctness(self):
		field = ChoiceWithDefault(default="default", choices=[("V1", "Value1"), ("V2", "Value2")])

		assert field.clean(None) == "default"
		assert field.clean("V1") == "V1"
		assert field.clean("V2") == "V2"


class TestIntegerArrayField:
	def test___init__(self):
		field = IntegerArrayField()
		assert field.sep == "|"

		field = IntegerArrayField(sep=":", required=True, help_text="Help text")
		assert field.sep == ":"
		assert field.required and field.help_text == "Help text"

	def test_clean_correctness(self):
		field = IntegerArrayField(sep="|")
		assert field.clean(None) is None
		assert field.clean("10") == [10]
		assert field.clean("10|15|20") == [10, 15, 20]


class TestStringArrayField:
	def test___init__(self):
		field = StringArrayField()
		assert field.sep == "|" and field.strip

		field = StringArrayField(sep=":", strip=False, required=True, help_text="Help text")
		assert field.sep == ":" and not field.strip
		assert field.required and field.help_text == "Help text"

	@pytest.mark.parametrize(
		"sep, strip, value, expected_result",
		[
			("|", True, None, None),
			("|", False, None, None),
			("|", True, "", [""]),
			("|", False, "", [""]),
			("|", True, "     \t\n", [""]),
			("|", False, "     \t\n", ["     \t\n"]),
			(";", False, "    value|value;value    ", ["    value|value", "value    "]),
		],
	)
	def test_clean_correctness(self, sep, strip, value, expected_result):
		field = StringArrayField(sep=sep, strip=strip)
		assert field.clean(value) == expected_result
