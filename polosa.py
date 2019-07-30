from contextlib import contextmanager
from datetime import datetime, timedelta


class _Polosa:
	def __init__(self, total=None, throttle_ms=200):
		self.start = datetime.now()
		self.last_update = None
		self.last_num = 0
		self.throttle_ms = throttle_ms
		self.total = total
		self.buf = ''

	def tick(self, num=None, caption=''):
		now = datetime.now()

		if num == None:
			self.last_num += 1
			num = self.last_num

		self.buf = f'{num}'
		if self.total != None:
			self.buf += f'/{self.total}'
		per_sec = num / (now - self.start).total_seconds()
		self.buf += f'   {per_sec:.1f}/sec   {caption}'

		if (self.last_update != None) and (now - self.last_update < timedelta(milliseconds=self.throttle_ms)):
			return

		print(self.buf, end='   \r')
		self.last_update = now

	def _finalize(self):
		print(self.buf)


@contextmanager
def polosa(*args, **kwargs):
	p = _Polosa(*args, **kwargs)
	try:
		yield p
	finally:
		p._finalize()


# print('==> Doing important stuff...')
# N = 2_000_000
# with polosa(total=N) as p:
# 	for i in range(0, N):
# 		p.tick(i+1, f'real index is {i}')
# print('==> All done!')

