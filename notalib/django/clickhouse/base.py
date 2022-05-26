from .profiler import before_cursor_execute, after_cursor_execute

import logging; log = logging.getLogger(__name__)

from notalib.time import Timing
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from django.conf import settings


CLICKHOUSE_URL = settings.CLICKHOUSE_URL
CLICKHOUSE_PROFILE = settings.CLICKHOUSE_PROFILE


# Activate profiler if needed
event.listens_for(Engine, "before_cursor_execute")(before_cursor_execute)
event.listens_for(Engine, "after_cursor_execute")(after_cursor_execute)


# Initialize engine
engine = create_engine(
	CLICKHOUSE_URL,
	pool_size=20,
	pool_pre_ping=False,
	echo=False,
)


def get_connection():
	return engine.connect()


def get_database_name() -> str:
	return engine.url.database


class Query:
	def __init__(self, q=None, **kwargs):
		self.q = q
		self.params = kwargs

	def execute(self):
		conn = get_connection()
		#if CLICKHOUSE_PROFILE: print(str(self.q))
		t = Timing(auto_print=False)
		with t:
			result = conn.execute(self.q, self.params).fetchall()
		return result

	def execute_val(self):
		rows = self.execute()
		assert len(rows) == 1, 'Expected to get exactly one row'
		assert len(rows[0]) == 1, 'Expected to get exactly one value'
		return rows[0][0]

	def execute_list(self):
		rows = self.execute()
		ret = []
		for row in rows:
			ret.append(row[0])
		return ret

	def execute_kv(self):
		rows = self.execute()
		ret = {}
		for row in rows:
			ret[row[0]] = row[1]
		return ret

	def execute_na(self):
		conn = get_connection()
		#if CLICKHOUSE_PROFILE: print(str(self.q))
		t = Timing(auto_print=False)
		with t:
			result = conn.execute(self.q, self.params)
		return result.rowcount
