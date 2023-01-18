import logging
from blessings import Terminal; t = Terminal()
from datetime import datetime


class ColorFormatter(logging.Formatter):
	"""
	Logging config example (settings.py):
	
	LOGGING = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'colors': {
				'()': 'util.colorlog.ColorFormatter',
			},
			'stamp': {
				'format': '%(asctime)s %(name)s [%(levelname)s] %(message)s',
				# 'format': '%(asctime)s %(name)s %(module)s [%(levelname)s] %(message)s',
			},
		},
		'handlers': {
			'console': {
				'class': 'logging.StreamHandler',
				'formatter': 'colors',
			},
		},
		'loggers': {
			# 'django': {
			# 	'handlers': ['console'],
			# 	'level': 'DEBUG',
			# },
			'dialer': {
				'handlers': ['console'],
				'level': 'DEBUG',
			},
		},
	}
	"""
	LOG_LEVEL_COLORS = {
		'DEBUG': t.white('DBG'),
		'INFO': t.blue('INF'),
		'WARNING': t.yellow('WRN'),
		'ERROR': t.red('ERR'),
		'CRITICAL': t.bright_red('CRT'),
	}
	NAME_LENGTH_MAX = 19

	def __init__(self, *args, **kwargs):
		super(ColorFormatter, self).__init__()

	def format(self, record) -> str:
		lvl = record.levelname
		lvl = self.LOG_LEVEL_COLORS.get(lvl, lvl)
		name = record.name

		if len(name) > self.NAME_LENGTH_MAX:
			name = name[-self.NAME_LENGTH_MAX:]

		return f'{datetime.strftime(datetime.now(), "%H:%M:%S.%f")}|{name}[{lvl}] {record.getMessage()}'
