from typing import Callable, Type
from warnings import warn


def deprecated(
	reason: str = 'Unspecified reason',
	warning: Type[DeprecationWarning] = DeprecationWarning,
	stacklevel: int = 2,
) -> Callable:
	"""
	Marks function or method as deprecated.

	Args:
		reason: The reason why the code has become deprecated.
		warning: Deprecated code warning class.
		stacklevel: Logging stacklevel.

	Note:
		See more about stacklevel in official docs:
			Logging: https://docs.python.org/3/library/logging.html#logging.Logger.debug
			Warnings: https://docs.python.org/3/library/warnings.html#warnings.warn
	"""
	def decorator(func: Callable):
		if not callable(func):
			raise TypeError('The "func" argument must be of Callable type')

		def inner(*args, **kwargs):
			warn(reason, warning, stacklevel=stacklevel)
			return func(*args, **kwargs)

		return inner

	return decorator
