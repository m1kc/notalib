from ..date import parse_month

from typing import Tuple, Optional, List

from django import forms


class MonthField(forms.CharField):
	def clean(self, value: Optional[str]) -> Optional[Tuple[int, int]]:
		if value is None:
			return None

		try:
			return parse_month(value)
		except:
			raise forms.ValidationError('Not a valid month (expected YYYY-MM)')


class ChoiceWithDefault(forms.ChoiceField):
	def __init__(self, *args, **kwargs):
		default_value = kwargs['default']
		del kwargs['default']
		super(ChoiceWithDefault, self).__init__(*args, **kwargs)
		self.default_value = default_value

	def clean(self, value: Optional[str]):
		if value is None:
			return self.default_value
		return super(ChoiceWithDefault, self).clean(value)


class IntegerArrayField(forms.CharField):
	def __init__(self, sep: str = '|', *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.sep = sep

	def clean(self, value: Optional[str]) -> Optional[List[int]]:
		if value is None:
			return None
		return list(map(int, value.split(self.sep)))


class StringArrayField(forms.CharField):
	def __init__(self, sep: str = '|', strip: bool = True, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.sep = sep
		self.strip = strip

	def clean(self, value: Optional[str]) -> Optional[List[str]]:
		if value is None:
			return None

		ret = value.split(self.sep)

		if self.strip:
			ret = list(map(lambda x: x.strip(), ret))

		return ret


class MonthArrayField(forms.CharField):
	def __init__(self, sep='|', *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.sep = sep

	def clean(self, value: Optional[str]) -> Optional[List[Tuple[int, int]]]:
		if value is None:
			return None

		value = value.split('|')

		try:
			return list(map(lambda x: parse_month(x), value))
		except:
			raise forms.ValidationError('Not a valid month (expected YYYY-MM)')
