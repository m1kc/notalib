from notalib.time import Timing

from unittest.mock import patch

from arrow import get


class TestTiming:
	def test___init__(self):
		timing = Timing()
		assert not timing.auto_print
		assert timing.result is None
		assert timing._start is None

		timing = Timing(True)
		assert timing.auto_print
		assert timing.result is None
		assert timing._start is None

	def test_context_manager(self, capsys):
		timing = Timing()
		start_arrow = get(2024, 1, 1, 15, 15, 15)
		end_arrow = get(2024, 1, 1, 15, 30, 15)

		with patch("arrow.now") as arrow_now:
			arrow_now.return_value = start_arrow
			timing.__enter__()
			assert timing._start == start_arrow

			arrow_now.return_value = end_arrow
			timing.__exit__(None, None, None)
			captured = capsys.readouterr()
			assert captured.out == ""

			timing.auto_print = True
			timing.__exit__(None, None, None)
			captured = capsys.readouterr()
			assert captured.out == "time: 0:15:00\n"
