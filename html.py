from html.parser import HTMLParser

import re

REGEX = re.compile('<[^>]*>')

class MLStripper(HTMLParser):
	def __init__(self):
		super().__init__()
		self.reset()
		self.strict = False
		self.convert_charrefs = True
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ' '.join(self.fed)

def strip_tags(s, fast_and_dirty=False):
	if fast_and_dirty:
		return REGEX.sub(' ', s)
	else:
		p = MLStripper()
		p.feed(s)
		return p.get_data()
	
	
class TablePrinter():
	def __init__(self, cols=(), use_attrs=False):
		self.cols = cols
		self._get = getattr if use_attrs else lambda arr, i: arr[i]

	def header(self): return '<table><thead><tr>' + ''.join(f'<th>{col}</th>' for col in self.cols) + '</tr></thead><tbody>'
	def entry(self, x): return '<tr>' + ''.join(f'<td>{self._get(x, col)}</td>' for col in self.cols) + '</tr>\n'
	def footer(self): return '</tbody></table>'

	def iterator_over(self, collection, data_only=False):
		if not data_only: yield self.header()
		for i in collection: yield self.entry(i)
		if not data_only: yield self.footer()
