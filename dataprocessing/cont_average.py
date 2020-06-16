

class ContAverage():
	def __init__(self, data = None):
		self.reset(data)

	def reset(self, data = None):
		self._count = 0
		self._sum = 0
		if isinstance(data, int):
			self._sum = data
			self._count = 1
		elif isinstance(data, list) or isinstance(data, tuple):
			self._sum = sum(data)
			self._count = len(data)

	def update(self, data):
		if isinstance(data, int):
			self._sum += data
			self._count += 1
		elif isinstance(data, list) or isinstance(data, tuple):
			self._sum += sum(data)
			self._count += len(data)

	def current_sum(self):
		return self._sum

	def current_count(self):
		return self._count

	def result(self):
		if self._count:
			return self._sum / self._count
		else:
			return None