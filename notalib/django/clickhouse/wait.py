from .mutations import is_mutations_running

from time import sleep
from typing import Union


def wait_result(db_name: str, table_name: str, delay: Union[int, float] = 0.25) -> None:
	"""
	Suspends the program while there are incomplete mutant processes.

	Args:
		db_name: Database name in which the deletion operation was performed.
		table_name: Table name in the {db_name} database in which the deletion operation was performed.
		delay: Delay between system table polls.

	Notes:
		Imagine that you are driving in a car to a railway crossing. A train is going to cross you by rail.
		This function is a handbrake that will save you from crashing.
	"""
	while is_mutations_running(db_name, table_name):
		sleep(delay)
