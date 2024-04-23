from notalib.polosa import polosa, _Polosa

from datetime import datetime

import pytest
from unittest.mock import patch


def finalize_spy(self):
	self.__finalize_call_times = getattr(self, '__finalize_call_times', 0) + 1


def test_polosa():
	with patch("notalib.polosa._Polosa._finalize", new=finalize_spy):
		with polosa(total=1, throttle_ms=200) as p:
			assert isinstance(p, _Polosa)

	assert getattr(p, '__finalize_call_times', None) == 1


class Test_Polosa:
	def test___init__(self):
		start_dt = datetime(2024, 1, 1)

		with patch("notalib.polosa.datetime") as polosa_datetime:
			polosa_datetime.now.return_value = start_dt

			p = _Polosa()
			assert p.start == start_dt
			assert p.last_update is None
			assert p.last_num == 0
			assert p.throttle_ms == 200
			assert p.total is None
			assert p.buf == ''

			p = _Polosa(total=2000, throttle_ms=999)
			assert p.start == start_dt
			assert p.last_update is None
			assert p.last_num == 0
			assert p.throttle_ms == 999
			assert p.total == 2000
			assert p.buf == ''

	@pytest.mark.parametrize(
		"total, throttle_ms, ticks, expected_stdouts",
		[
			(None, 200, [(), ()], ["1   0.1/sec      \r", "2   0.0/sec      \r"]),
			(200, 200, [(), ()], ["1/200   0.1/sec      \r", "2/200   0.0/sec      \r"]),
			(200, 200, [(20, ""), (40, "caption")], ["20/200   2.0/sec      \r", "40/200   0.9/sec   caption   \r"]),
			(200, 200000, [(20, ""), (40, "caption")], ["20/200   2.0/sec      \r", ""]),
		],
	)
	def test_tick(self, total, throttle_ms, ticks, expected_stdouts, capsys):
		with patch("notalib.polosa.datetime") as polosa_datetime:
			polosa_datetime.now.return_value = datetime(2024, 1, 1, 10, 30, 30)
			p = _Polosa(total, throttle_ms)

			polosa_datetime.now.return_value = datetime(2024, 1, 1, 10, 30, 40)
			p.tick(*ticks[0])
			captured = capsys.readouterr()
			assert captured.out == expected_stdouts[0]

			polosa_datetime.now.return_value = datetime(2024, 1, 1, 10, 31, 15)
			p.tick(*ticks[1])
			captured = capsys.readouterr()
			assert captured.out == expected_stdouts[1]



	def test__finalize(self, capsys):
		p = _Polosa()
		p.buf = "hello world"
		p._finalize()
		captured = capsys.readouterr()
		assert captured.out == "hello world\n"
