import re
from typing import Generator, Iterable
from html.parser import HTMLParser


REGEX = re.compile('<[^>]*>')


class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.fed = []

	def handle_data(self, data: str) -> None:
		self.fed.append(data)

	def get_data(self) -> str:
		return ' '.join(self.fed)


def strip_tags(s: str, fast_and_dirty: bool = False) -> str:
	if fast_and_dirty:
		return REGEX.sub(' ', s)

	p = MLStripper()
	p.feed(s)

	return p.get_data()


class TablePrinter:
	"""
	Prints an HTML table, row by row, from the given data, using attrs or dictionary keys as columns.

	Two ways to use it:
	* Call header() / entry() / footer() manually

	Examples:
		>>> from notalib.hypertext import TablePrinter
		>>> t = TablePrinter(['a', 'b'])
		>>> t.header()
		'<table><thead><tr><th>a</th><th>b</th></tr></thead><tbody>'
		>>> t.entry({'a': 1, 'b': 2})
		'<tr><td>1</td><td>2</td></tr>\n'
		>>> t.entry({'a': 11, 'b': 22})
		'<tr><td>11</td><td>22</td></tr>\n'
		>>> t.footer()
		'</tbody></table>'

		>>> # Pass an iterable to iterator_over()
		>>> from notalib.hypertext import TablePrinter
		>>> t = TablePrinter(['a', 'b'])
		>>> list(t.iterator_over([ {'a': 11, 'b': 22} ]))
		['<table><thead><tr><th>a</th><th>b</th></tr></thead><tbody>', '<tr><td>11</td><td>22</td></tr>\n', '</tbody></table>']
	"""
	def __init__(self, cols=(), use_attrs=False) -> None:
		self.cols = cols
		self._get = getattr if use_attrs else lambda arr, i: arr[i]

	def header(self) -> str:
		return '<table><thead><tr>' + ''.join(f'<th>{col}</th>' for col in self.cols) + '</tr></thead><tbody>'

	def entry(self, x) -> str:
		return '<tr>' + ''.join(f'<td>{self._get(x, col)}</td>' for col in self.cols) + '</tr>\n'

	def footer(self) -> str:
		return '</tbody></table>'

	def iterator_over(self, collection: Iterable, data_only: bool = False) -> Generator:
		if not data_only:
			yield self.header()

		for i in collection:
			yield self.entry(i)

		if not data_only:
			yield self.footer()
