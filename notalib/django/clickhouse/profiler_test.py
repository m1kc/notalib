from notalib.django.clickhouse.profiler import indent, midrange_cut, before_cursor_execute, after_cursor_execute

from unittest.mock import patch
from typing import Optional

import pytest


class FakeContext:
	_query_start_time: Optional[float]

	def __init__(self) -> None:
		self._query_start_time = None


@pytest.mark.parametrize(
	"level, text, expected_result",
	[
		(0, "Hello World", "Hello World"),
		(0, "Hello\nWorld", "Hello\nWorld"),
		(4, "Hello World", "    Hello World"),
		(4, "Hello\nWorld", "    Hello\n    World"),
	],
)
def test_indent(level, text, expected_result):
	assert indent(level, text) == expected_result


@pytest.mark.parametrize(
	"text, max_length, expected_result",
	[
		("", 0, ""),
		("Hello World", 0, "\n...\nHello World"),
		("Hello World", 5, "Hello\n...\nHello World"),
		("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", 20, "Lorem ipsum dolor \n...\nt.")
	]
)
def test_midrange_cut(text, max_length, expected_result):
	assert midrange_cut(text, max_length) == expected_result


def test_before_cursor_execute():
	context = FakeContext()

	with patch("notalib.django.clickhouse.profiler.CLICKHOUSE_PROFILE", new=False):
		assert before_cursor_execute(None, None, None, None, context, None) is None
		assert context._query_start_time is None

	with patch("notalib.django.clickhouse.profiler.CLICKHOUSE_PROFILE", new=True):
		with patch("time.time") as time:
			time.return_value = 15.11
			before_cursor_execute(None, None, None, None, context, None)
			assert context._query_start_time == 15.11


def test_after_cursor_execute(capsys):
	context = FakeContext()

	with patch("notalib.django.clickhouse.profiler.CLICKHOUSE_PROFILE", new=False):
		assert after_cursor_execute(None, None, "", [], context, None) is None
		captured = capsys.readouterr()
		assert not captured.out

	with patch("notalib.django.clickhouse.profiler.CLICKHOUSE_PROFILE", new=True):
		context._query_start_time = 911.007141

		with patch("time.time") as time:
			time.return_value = 911.314518
			after_cursor_execute(None, None, "TEST Statement", ["TEST", "PARAM"], context, None)
			captured = capsys.readouterr()
			assert captured.out == "\nQuery:  TEST Statement\nparams: ['TEST', 'PARAM']\n-- time: 307.38ms ------------------------------\n\n"
