from notalib.django.clickhouse.mutations import get_mutations_in_progress_count, is_mutations_running
from notalib.django.clickhouse.base import Query

from unittest.mock import patch, Mock


def make_fake_query():
	class FakeQuery(Query):
		instance = None

		def __new__(cls, *args, **kwargs) -> "FakeQuery":
			if cls.instance is None:
				cls.instance = super().__new__(cls, *args, **kwargs)

			return cls.instance

		def __init__(self, q=None, **kwargs):
			if not self is self.__class__.instance:
				super().__init__(q, **kwargs)

		def execute_val(self) -> None:
			return None

		def execute_list(self) -> None:
			return None


	return FakeQuery


def test_get_mutations_in_progress_count():
	FakeQuery = make_fake_query()

	with patch("notalib.django.clickhouse.mutations.Query", new=FakeQuery):
		database, table = "TEST_DATABASE", "TEST_TABLE"
		get_mutations_in_progress_count(database, table)
		query = FakeQuery()

		assert query.params == {'db_name': database, 'table_name': table}


def test_is_mutations_running():
	FakeQuery = make_fake_query()

	with patch("notalib.django.clickhouse.mutations.Query", new=FakeQuery):
		database, table = "TEST_DATABASE", "TEST_TABLE"
		is_mutations_running(database, table)
		query = FakeQuery()

		assert query.params == {"db_name": database, "table_name": table}
