from notalib.django.clickhouse.wait import wait_result
from notalib.test_fakes import FakeFunction, SequenceFakeFunction

from unittest.mock import patch


def test_wait_result():
	is_mutations_running_fn = SequenceFakeFunction([True, False])
	sleep_fn = FakeFunction()

	with patch("notalib.django.clickhouse.wait.is_mutations_running", new=is_mutations_running_fn):
		with patch("notalib.django.clickhouse.wait.sleep", new=sleep_fn):
			database, table, delay = "TEST_DATABASE", "TEST_TABLE", 5

			wait_result(database, table, delay)
			assert is_mutations_running_fn.last_call_args == (database, table)
			assert is_mutations_running_fn.call_count == 2

			assert sleep_fn.last_call_args == (delay, )
			assert sleep_fn.call_count == 1
