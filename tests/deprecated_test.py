from notalib.deprecated import deprecated

import pytest


def test_deprecated():
	func = deprecated()(lambda: None)

	with pytest.warns(DeprecationWarning):
		func()
