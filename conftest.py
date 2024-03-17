import sys
from typing import Callable

from django.conf import settings


class Blessings:
	class Terminal:
		def __init__(self):
			self.colors = {}

		def white(self, lvl: str) -> str:
			self.colors['white'] = lvl
			return lvl

		def blue(self, lvl: str) -> str:
			self.colors['blue'] = lvl
			return lvl

		def yellow(self, lvl: str) -> str:
			self.colors['yellow'] = lvl
			return lvl

		def red(self, lvl: str) -> str:
			self.colors['red'] = lvl
			return lvl

		def bright_red(self, lvl: str) -> str:
			self.colors['bright_red'] = lvl
			return lvl


class SQLAlchemyEngine:
	def __init__(self, *args, **kwargs) -> None:
		self.args = args
		self.kwargs = kwargs


class SQLAlchemyEvent:
	listened_events = []

	@classmethod
	def listens_for(cls, engine: SQLAlchemyEngine, label: str):
		def inner(callback: Callable):
			cls.listened_events.append((engine, label, callback))

		return inner


class SQLAlchemyQuery:
	def __init__(self, *args, **kwargs) -> None:
		self.args = args
		self.kwargs = kwargs


class SQLAlchemyModule:
	create_engine = lambda *args, **kwargs: SQLAlchemyEngine(*args, **kwargs)
	event = SQLAlchemyEvent


class SQLAlchemyEngineModule:
	Engine = SQLAlchemyEngine


class SQLAlchemySQLModule:
	text = SQLAlchemyQuery


def pytest_configure():
	settings.configure(
		USE_I18N=False,
		INSTALLED_APPS=[
			"django.contrib.contenttypes",
			"django.contrib.auth",
			"notalib.django_xauth",
		],
		CLICKHOUSE_PROFILE=False,
		CLICKHOUSE_URL="clickhouse+native://localhost/default"
	)

	sys.modules["blessings"] = Blessings
	sys.modules["sqlalchemy"] = SQLAlchemyModule
	sys.modules["sqlalchemy.engine"] = SQLAlchemyEngineModule
	sys.modules["sqlalchemy.sql"] = SQLAlchemySQLModule
