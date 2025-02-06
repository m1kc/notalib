from .base import Query

from sqlalchemy.sql import text


def get_mutations_in_progress_count(db_name: str, table_name: str) -> int:
	"""
	Requests from the System.Mutants table the number of mutations in progress.

	Args:
		db_name: Must contain name of existed database with tables.
		table_name: Must contain name of existed table in database with db_name.

	Returns:
		Number of mutants in progress.
	"""

	# TODO: Find a way to use FROM construction. By default, requests are redirected to the DB specified during
	#  connection
	# query = Query(
	# 	select([func.count(System_Mutations)])
	#
	# 	.where('database' == db_name)
	# 	.where('table' == 'order')
	# 	.where('is_done' == 0)
	# 	.group_by('is_done')
	# )

	query = Query()
	query.q = text("""SELECT count(*)
FROM system.mutations
WHERE database == :db_name AND table == :table_name AND is_done == 0""")

	query.params = {'db_name': db_name, 'table_name': table_name}

	return query.execute_val()


def is_mutations_running(db_name: str, table_name: str) -> bool:
	"""
	Checks for the presence of running mutations.

	Args:
		db_name: Name of database to check.
		table_name: Name of table to check.

	Returns:
		Returns True if there are running mutations, otherwise False.
	"""
	query = Query()
	query.q = text("""\
SELECT 1
FROM system.mutations
WHERE database = :db_name AND table = :table_name AND is_done = 0
LIMIT 1
""")
	query.params = {"db_name": db_name, "table_name": table_name}

	return bool(query.execute_list())
