from notalib.django.clickhouse.wait import wait_result
from notalib.test_fakes import FakeFunction, SequenceFakeFunction

from unittest.mock import patch


def test_wait_result():
	get_mutations_count_fn = SequenceFakeFunction([5, 0])
	sleep_fn = FakeFunction()

	with patch("notalib.django.clickhouse.wait.get_mutations_in_progress_count", new=get_mutations_count_fn):
		with patch("notalib.django.clickhouse.wait.sleep", new=sleep_fn):
			database, table, delay = "TEST_DATABASE", "TEST_TABLE", 5

			wait_result(database, table, delay)
			assert get_mutations_count_fn.last_call_args == (database, table)
			assert get_mutations_count_fn.call_count == 2

			assert sleep_fn.last_call_args == (delay, )
			assert sleep_fn.call_count == 1
