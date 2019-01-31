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
