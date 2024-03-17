from notalib.trendsetter import Unit, SimpleUnit, to_unit, Trendsetter
from notalib.test_fakes import FakeFunction

import pytest


class TestUnit:
	def test_execute(self):
		with pytest.raises(NotImplementedError):
			Unit().execute(None, None, None)


class TestSimpleUnit:
	def test___init__(self):
		unit = SimpleUnit(None)
		assert unit.execute_fn is None

		unit = SimpleUnit(lambda x: None)
		assert callable(unit.execute_fn)

	def test_execute(self):
		function_spy = FakeFunction(123)
		unit = SimpleUnit(function_spy)
		assert unit.execute() == 123
		assert function_spy.call_count == 1
		assert function_spy.last_call_args == ()
		assert function_spy.last_call_kwargs == {}

		assert unit.execute(1, 2, 3) == 123
		assert function_spy.call_count == 2
		assert function_spy.last_call_args == (1, 2, 3)
		assert function_spy.last_call_kwargs == {}


def test_to_unit():
	function_spy = FakeFunction(123)
	unit = to_unit(function_spy)
	assert isinstance(unit, SimpleUnit)
	assert unit.execute_fn is function_spy


class TestTrendsetter:
	def test___init__(self):
		trendsetter = Trendsetter()
		assert trendsetter.units == {}
		assert trendsetter.unit_deps == {}
		assert trendsetter.options == {}
		assert trendsetter.cache == {}

		options = {"option1": None, "option2": 1}
		trendsetter = Trendsetter(options)
		assert trendsetter.units == {}
		assert trendsetter.unit_deps == {}
		assert trendsetter.options == options
		assert trendsetter.cache == {}

	def test_register(self):
		trendsetter = Trendsetter()
		unit1 = Unit()
		assert trendsetter.register("unit1", unit1) is None
		assert trendsetter.units["unit1"] is unit1
		assert trendsetter.unit_deps["unit1"] == []

		unit2 = Unit()
		assert trendsetter.register("unit2", unit2, ["unit1"]) is None
		assert trendsetter.units["unit2"] is unit2
		assert trendsetter.unit_deps["unit2"] == ["unit1"]

		assert trendsetter.register("unit1", unit2) is None
		assert trendsetter.units["unit1"] is unit2

	def test_get(self):
		options = {"option1": None, "option2": 1}
		trendsetter = Trendsetter(options)
		function_spy = FakeFunction(123)
		unit1 = SimpleUnit(FakeFunction(321))
		trendsetter.register("unit1", unit1)
		trendsetter.register("unit2", SimpleUnit(function_spy))

		with pytest.raises(KeyError):
			trendsetter.get("unexpected")

		assert trendsetter.get("unit2") == 123
		assert function_spy.call_count == 1
		assert function_spy.last_call_args == ("unit2", {}, options)

		del trendsetter.cache["unit2"]
		trendsetter.unit_deps["unit2"] = ["unit1"]
		assert trendsetter.get("unit2") == 123
		assert function_spy.call_count == 2
		assert function_spy.last_call_args == ("unit2", {"unit1": 321}, options)

		function_spy.return_value = "Hello World"
		assert trendsetter.get("unit2") == 123
		assert function_spy.call_count == 2
		assert function_spy.last_call_args == ("unit2", {"unit1": 321}, options)
