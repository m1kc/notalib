from notalib.trendsetter import Unit, Trendsetter, SimpleUnit

from abc import ABC, abstractmethod


class Adder(ABC):
	@abstractmethod
	def add(self, a, b): ...


class AdderImpl(Adder):
	def add(self, a, b):
		return a + b


class ExperimentalAdderImpl(Adder):
	def add(self, a, b):
		return a  # TODO


class AdderUnit(Unit):
	def execute(self, name, deps, options):
		if options['use_experimental_adder']:
			return ExperimentalAdderImpl()
		else:
			return AdderImpl()


class Fibonacci:
	def __init__(self, adder: Adder):
		self.adder = adder

	def compute(self, n):
		if n <= 2:
			return 1

		return self.adder.add(self.compute(n - 1), self.compute(n - 2))


def test_trendsetter():
	ts = Trendsetter({
		# No assumptions what your options look like.
		'use_experimental_adder': False
	})
	ts.register('Adder', AdderUnit())
	ts.register(
		'Fibonacci',
		# Simplified interface for more straightforward cases
		SimpleUnit(lambda name, deps, options: Fibonacci(deps['Adder'])),
		# List of dependencies - they will be instantiated first
		['Adder'],
	)

	# TODO: Eliminate the contract breach.
	assert ts.get('Adder').add(2, 2) == 4
	assert ts.get('Fibonacci').compute(6) == 8
