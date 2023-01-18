import arrow


class Timing:
	"""
	Measures time that an operation took to complete.

	Examples:
		>>> timing = Timing(auto_print=True)
		>>> with timing:
		>>> 	# do something

		>>> timing = Timing()
		>>> with timing:
		>>> 	# do something
		>>> print(timing.result)
	"""
	def __init__(self, auto_print: bool = False) -> None:
		self.result = None
		self._start = None
		self.auto_print = auto_print

	def __enter__(self) -> None:
		self._start = arrow.now()

	def __exit__(self, exc_type, exc_value, traceback) -> None:
		self.result = arrow.now() - self._start

		if self.auto_print:
			print('time:', self.result)
