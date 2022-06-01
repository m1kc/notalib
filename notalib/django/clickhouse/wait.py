from .mutations import get_mutations_in_progress_count

from time import sleep
from typing import Union


def wait_result(db_name: str, table_name: str, delay: Union[int, float] = 0.25) -> None:
	"""
	Suspends the program while there are incomplete mutant processes.

	Parameters
	----------
	db_name: str
		Database name in which the deletion operation was performed.
	table_name: str
		Table name in the {db_name} database in which the deletion operation was performed.
	delay: Union[int, float]
		Delay between system table polls.

	Notes
	-----
	Imagine that you are driving in a car to a railway crossing. A train is going to cross you by rail.
	This function is a handbrake that will save you from crashing.
	"""

	while get_mutations_in_progress_count(db_name, table_name):
		sleep(delay)
