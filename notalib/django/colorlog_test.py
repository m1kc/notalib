from notalib.django.colorlog import ColorFormatter

from unittest.mock import patch
from logging import LogRecord, DEBUG, INFO, WARNING, ERROR, CRITICAL

import pytest
from blessings import Terminal; t = Terminal()


class TestColorFormatter:
	@pytest.mark.parametrize(
		"record, expected_message",
		[
			(LogRecord('NAME', DEBUG, 'pathname', 0, 'MESSAGE', [], None), "12:30:30.500|NAME[DBG] MESSAGE"),
			(LogRecord('NAME', INFO, 'pathname', 0, 'MESSAGE', [], None), "12:30:30.500|NAME[INF] MESSAGE"),
			(LogRecord('NAME', WARNING, 'pathname', 0, 'MESSAGE', [], None), "12:30:30.500|NAME[WRN] MESSAGE"),
			(LogRecord('NAME', ERROR, 'pathname', 0, 'MESSAGE', [], None), "12:30:30.500|NAME[ERR] MESSAGE"),
			(LogRecord('NAME', CRITICAL, 'pathname', 0, 'MESSAGE', [], None), "12:30:30.500|NAME[CRT] MESSAGE"),
			(
				LogRecord('LONG-LONG-LONG-LONG NAME', CRITICAL, 'pathname', 0, 'MESSAGE', [], None),
				"12:30:30.500|LONG-LONG-LONG NAME[CRT] MESSAGE",
			),
		],
	)
	def test_format(self, record, expected_message):
		formatter = ColorFormatter()

		with patch("notalib.django.colorlog.datetime") as datetime_mock:
			datetime_mock.strftime.return_value = "12:30:30.500"
			assert formatter.format(record) == expected_message
