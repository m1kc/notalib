from notalib.django.clickhouse.mutations import get_mutations_in_progress_count
from notalib.django.clickhouse.base import Query

from unittest.mock import patch


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


def test_get_mutations_in_progress_count():
	with patch("notalib.django.clickhouse.mutations.Query", new=FakeQuery):
		database, table = "TEST_DATABASE", "TEST_TABLE"
		get_mutations_in_progress_count(database, table)
		query = FakeQuery()

		assert query.params == {'db_name': database, 'table_name': table}
