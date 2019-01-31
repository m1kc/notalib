import logging
from blessings import Terminal; t = Terminal()
from datetime import datetime


class ColorFormatter(logging.Formatter):
	def __init__(self, *args, **kwargs):
		super(ColorFormatter, self).__init__()

	def format(self, record):
		lvl = record.levelname
		if record.levelname == 'DEBUG': lvl = t.white('DBG')
		if record.levelname == 'INFO': lvl = t.blue('INF')
		if record.levelname == 'WARNING': lvl = t.yellow('WRN')
		if record.levelname == 'ERROR': lvl = t.red('ERR')
		if record.levelname == 'CRITICAL': lvl = t.bright_red('CRT')

		NAME_LENGTH_MAX = 19
		name = record.name
		if len(name) > NAME_LENGTH_MAX:
			name = name[-NAME_LENGTH_MAX:]

		return f'{datetime.strftime(datetime.now(), "%H:%M:%S.%f")}|{name}[{lvl}] {record.getMessage()}'
