from .base import Query

from sqlalchemy.sql import text


def get_mutations_in_progress_count(db_name: str, table_name: str) -> int:
	"""
	Requests from the System.Mutants table the number of mutations in progress.

	Parameters
	----------
	db_name: str
		Must contain name of existed database with tables.
	table_name: str
		Must contain name of existed table in database with db_name.

	Returns
	-------
	int
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
