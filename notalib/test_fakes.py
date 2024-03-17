from typing import Sequence


class FakeFunction:
	"""
	Returns specified data during call and remembers call parameters.
	"""
	def __init__(self, return_value = None):
		self.return_value = return_value
		self.call_count = 0
		self.last_call_args = ()
		self.last_call_kwargs = {}

	def __call__(self, *args, **kwargs):
		self.last_call_args = args
		self.last_call_kwargs = kwargs
		self.call_count += 1
		return self.return_value


class SequenceFakeFunction(FakeFunction):
	"""
	Returns a specified data element depending on the call number and remembers call parameters.
	"""
	def __init__(self, return_value=None):
		if not isinstance(return_value, Sequence) and return_value is not None:
			raise TypeError("Unexpected type of return value (allowed: Sequence[any] or None)")

		super().__init__(return_value or [None])
		self.call_args = []
		self.call_kwargs = []

	def __call__(self, *args, **kwargs):
		return_value: Sequence = super().__call__(*args, **kwargs)		# type: ignore

		self.call_args.append(self.last_call_args)
		self.call_kwargs.append(self.last_call_kwargs)

		return return_value[self.call_count - 1]
