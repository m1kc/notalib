from notalib.deprecated import deprecated

import pytest


class TestDeprecated:
	def test_exception(self):
		with pytest.raises(TypeError, match='The "func" argument must be of Callable type'):
			deprecated()("wrong argument")

	@pytest.mark.filterwarnings("ignore:deprecated")
	def test_function_decoration(self):
		with pytest.deprecated_call(match="Unspecified reason"):
			deprecated()(lambda: None)()

	@pytest.mark.filterwarnings("ignore:deprecated")
	def test_method_decoration(self):
		class T:
			@deprecated()
			def method(self):
				pass

		with pytest.deprecated_call(match="Unspecified reason"):
			T().method()

	@pytest.mark.filterwarnings("ignore:deprecated")
	def test_custom_args(self):
		with pytest.warns(UserWarning, match="hello world"):
			deprecated(reason="hello world", warning=UserWarning)(lambda: None)()
