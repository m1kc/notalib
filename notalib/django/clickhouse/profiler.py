import time
import logging; log = logging.getLogger(__name__)

from django.conf import settings


CLICKHOUSE_PROFILE = settings.CLICKHOUSE_PROFILE


########
# How to use:
#
# from .clickhouse_profiler import before_cursor_execute, after_cursor_execute
# ...
# event.listens_for(Engine, "before_cursor_execute")(before_cursor_execute)
# event.listens_for(Engine, "after_cursor_execute")(after_cursor_execute)
########


def indent(n: int, s: str):
	padding = ' '*n
	return '\n'.join(map(lambda x: padding+x, s.split('\n')))


def midrange_cut(s: str, n: int):
	if len(s) <= n:
		return s
	right = n // 10
	left = n - right
	ret = s[:left] + '\n...\n' + s[-right:]
	return ret


#@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
	if not CLICKHOUSE_PROFILE: return
	context._query_start_time = time.time()


#@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
	if not CLICKHOUSE_PROFILE: return
	total = time.time() - context._query_start_time

	parameters_s = midrange_cut(str(parameters), 200)
	statement_s = midrange_cut(statement, 500)

	s = f'''
Query:  {indent(8, statement_s).strip()}
params: {indent(8, parameters_s).strip()}
-- time: {"%.02fms" % (total*1000)} ------------------------------
'''
	print(s)
