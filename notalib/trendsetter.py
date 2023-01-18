from abc import ABC, abstractmethod
from typing import Callable, Optional, Hashable, TypeVar


CacheKey = TypeVar('CacheKey', bound=Hashable)


class Unit(ABC):
	@abstractmethod
	def execute(self, name, deps, options): ...


class SimpleUnit(Unit):
	def __init__(self, execute_fn: Callable):
		self.execute_fn = execute_fn

	def execute(self, *args):
		return self.execute_fn(*args)


class Trendsetter:
	"""
	Trendsetter deals with your complicated dependency tree where every
	interface has several implementations, chosen at runtime,
	with not-so-easy instantiation process for each - and does it lazily,
	and with caching (which doesn't prevent you from having several
	dependency trees, each one cached independently).
	"""
	def __init__(self, options: Optional[dict] = None) -> None:
		self.units = {}
		self.unit_deps = {}
		self.options = options or {}
		self.cache = {}

	def register(self, name: CacheKey, unit: Unit, deps: Optional[list] = None) -> None:
		self.units[name] = unit
		self.unit_deps[name] = deps or []

	def get(self, name: CacheKey) -> Unit:
		if name in self.cache:
			return self.cache[name]

		deps = {}

		for i in self.unit_deps[name]:
			deps[i] = self.get(i)

		ret = self.units[name].execute(name, deps, self.options)
		self.cache[name] = ret

		return ret
