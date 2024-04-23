from notalib.django.clickhouse.base import get_connection, get_database_name, Query
from notalib.test_fakes import FakeFunction

from unittest.mock import patch

import pytest


class SQLAlchemyEngineURL:
	def __init__(self, database: str) -> None:
		self.database = database


class SQLAlchemyCursorResult:
	def __init__(self) -> None:
		self.fetchall = FakeFunction()
		self.rowcount = 0


class SQLAlchemyConnection:
	def __init__(self) -> None:
		self.execute = FakeFunction(SQLAlchemyCursorResult())


def test_get_connection():
	connect_method = FakeFunction("CONNECTION")

	with patch("notalib.django.clickhouse.base.engine") as engine:
		engine.connect = connect_method
		assert get_connection() == "CONNECTION"
		assert connect_method.call_count == 1
		assert connect_method.last_call_args == tuple()


def test_get_database_name():
	with patch("notalib.django.clickhouse.base.engine") as engine:
		engine.url = SQLAlchemyEngineURL("TEST DATABASE")
		assert get_database_name() == "TEST DATABASE"


class TestQuery:
	def test___init__(self):
		query = Query()
		assert query.q is None
		assert query.params == {}

		query = Query("Q", a=1, b=2.2, c="test")
		assert query.q == "Q"
		assert query.params == {'a': 1, 'b': 2.2, 'c': "test"}

	def test_execute(self):
		with patch("notalib.django.clickhouse.base.get_connection") as get_connection:
			connection = SQLAlchemyConnection()
			get_connection.return_value = connection
			connection.execute.return_value.fetchall.return_value = "DATA"

			query = Query()
			assert query.execute() == "DATA"
			assert connection.execute.last_call_args == (query.q, query.params)
			assert connection.execute.call_count == 1
			assert connection.execute.return_value.fetchall.last_call_args == ()
			assert connection.execute.return_value.fetchall.call_count == 1

	def test_execute_val(self):
		query = Query()

		with patch.object(query, "execute") as execute:
			execute.return_value = []

			with pytest.raises(AssertionError, match="Expected to get exactly one row"):
				query.execute_val()

			execute.return_value = [[], []]

			with pytest.raises(AssertionError, match="Expected to get exactly one row"):
				query.execute_val()

			execute.return_value = [[]]

			with pytest.raises(AssertionError, match="Expected to get exactly one value"):
				query.execute_val()

			execute.return_value = [[None, None]]

			with pytest.raises(AssertionError, match="Expected to get exactly one value"):
				query.execute_val()

			execute.return_value = [["DATA"]]
			assert query.execute_val() == "DATA"

	def test_execute_list(self):
		query = Query()

		with patch.object(query, "execute") as execute:
			execute.return_value = []

			assert query.execute_list() == []

			execute.return_value = [[1, 2, 3], [4, 5, 6], ["Hello", "World", None]]
			assert query.execute_list() == [1, 4, "Hello"]

	def test_execute_kv(self):
		query = Query()

		with patch.object(query, "execute") as execute:
			execute.return_value = []

			assert query.execute_kv() == {}

			execute.return_value = [[1, 2, 3], [4, 5, 6], ["Hello", "World", None]]
			assert query.execute_kv() == {1: 2, 4: 5, "Hello": "World"}

	def test_execute_na(self):
		query = Query()

		with patch("notalib.django.clickhouse.base.get_connection") as get_connection:
			connection = SQLAlchemyConnection()
			get_connection.return_value = connection
			connection.execute.return_value.rowcount = 207

			assert query.execute_na() == 207
