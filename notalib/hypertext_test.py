from notalib.hypertext import MLStripper, TablePrinter, strip_tags
from notalib.test_fakes import FakeFunction

import pytest
from unittest.mock import patch


class RowData:
	def __init__(self, col1, col2, col3):
		self.col1 = col1
		self.col2 = col2
		self.col3 = col3


class TestMLStripper:
	def test___init__(self):
		stripper = MLStripper()
		assert not stripper.strict
		assert stripper.convert_charrefs
		assert stripper.fed == []

	def test_handle_data(self):
		stripper = MLStripper()
		stripper.handle_data("1")
		stripper.handle_data("2")
		stripper.handle_data("3")
		assert stripper.fed == ["1", "2", "3"]

	def test_get_data(self):
		stripper = MLStripper()
		assert stripper.get_data() == ""

		stripper.fed = ["1", "1", "1"]
		assert stripper.get_data() == "1 1 1"


class TestTablePrinter:
	def test___init__(self):
		printer = TablePrinter()
		assert printer.cols == ()
		assert printer._get is not getattr

		printer = TablePrinter(['col1', 'col2'], True)
		assert printer.cols == ['col1', 'col2']
		assert printer._get is getattr

	def test_header(self):
		printer = TablePrinter()
		assert printer.header() == "<table><thead><tr></tr></thead><tbody>"

		printer.cols = ("col1", "col2", "col3")
		expected_ths = map(lambda x: f"<th>{x}</th>", printer.cols)
		assert printer.header() == f"<table><thead><tr>{''.join(expected_ths)}</tr></thead><tbody>"

	@pytest.mark.parametrize(
		"cols, use_attrs, row_values, expected_result",
		[
			((), False, [], "<tr></tr>\n"),
			((), False, [1, 2, 3], "<tr></tr>\n"),
			((), True, [1, 2, 3], "<tr></tr>\n"),
			((0, 1, 2), False, [1, 2, 3], "<tr><td>1</td><td>2</td><td>3</td></tr>\n"),
			(
				("col1", "col2", "col3"),
				True,
				RowData(1, 2, 3),
				"<tr><td>1</td><td>2</td><td>3</td></tr>\n",
			),
		],
	)
	def test_entry(self, cols, use_attrs, row_values, expected_result):
		printer = TablePrinter(cols, use_attrs)
		assert printer.entry(row_values) == expected_result

	def test_footer(self):
		printer = TablePrinter()
		assert printer.footer() == '</tbody></table>'

	@pytest.mark.parametrize(
		"collection, data_only, expected_call_count",
		[
			([], False, (1, 0, 1)),
			([], True, (0, 0, 0)),
			([[], [], []], False, (1, 3, 1)),
			([[], [], []], True, (0, 3, 0)),
		],
	)
	def test_iterator_over(self, collection, data_only, expected_call_count):
		printer = TablePrinter()
		fake_header = FakeFunction()
		fake_entry = FakeFunction()
		fake_footer = FakeFunction()

		with patch.object(printer, "header", new=fake_header):
			with patch.object(printer, "entry", new=fake_entry):
				with patch.object(printer, "footer", new=fake_footer):
					list(printer.iterator_over(collection, data_only))
					assert fake_header.call_count == expected_call_count[0]
					assert fake_entry.call_count == expected_call_count[1]
					assert fake_footer.call_count == expected_call_count[2]


def test_strip_tags():
	assert strip_tags("<a>Link!</a>", True) == " Link! "
	assert strip_tags("<a>Link!</a>", False) == "Link!"

	assert strip_tags("<!-->Comment</-->", True) == " Comment "
	assert strip_tags("<!-->Comment</-->", False) == ""
