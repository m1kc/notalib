from .date import parse_month
from django import forms


class MonthField(forms.CharField):
	def clean(self, value):
		if value is None: return None
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

	def clean(self, value):
		if value is None:
			return self.default_value
		return super(ChoiceWithDefault, self).clean(value)
