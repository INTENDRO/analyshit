import statistics
import datetime
import collections
from enum import Enum
from .cont_average import ContAverage

MONTHS = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
WEEKDAYS = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
WEEKS = tuple(range(1,54))
DATES = tuple(datetime.date.fromordinal(datetime.date(2020,1,1).toordinal() + i).strftime("%y%m%d") for i in range(366))


class TimeSpan(Enum):
	DATE = 1
	WEEKDAY = 2
	WEEK = 3
	MONTH = 4

class TimeSpanAverage():
	def __init__(self, *, data = None, timespan = TimeSpan.DATE):
		self._avg = {}
		if timespan == TimeSpan.DATE:
			self._timespan_list = DATES
		elif timespan == TimeSpan.WEEKDAY:
			self._timespan_list = WEEKDAYS
		elif timespan == TimeSpan.WEEK:
			self._timespan_list = WEEKS
		elif timespan == TimeSpan.MONTH:
			self._timespan_list = MONTHS


		if isinstance(data, dict):
			self._avg = {timespan: ContAverage(data.get(timespan)) for timespan in self._timespan_list}
		else:
			self._avg = {timespan: ContAverage() for timespan in self._timespan_list}

	def reset(self, data = None):
		for timespan in self._timespan_list:
			self._avg[timespan].reset()

	def update(self, data):
		for timespan, value in data.items():
			self._avg[timespan].update(value)

	def result(self):
		return collections.OrderedDict((timespan, self._avg[timespan].result()) for timespan in self._timespan_list)

class TimeSpanList():
	def __init__(self, *, data = None, timespan = TimeSpan.DATE):
		self._avg = {}
		if timespan == TimeSpan.DATE:
			self._timespan_list = DATES
		elif timespan == TimeSpan.WEEKDAY:
			self._timespan_list = WEEKDAYS
		elif timespan == TimeSpan.WEEK:
			self._timespan_list = WEEKS
		elif timespan == TimeSpan.MONTH:
			self._timespan_list = MONTHS


		if isinstance(data, dict):
			self._avg = {timespan: data.get(timespan) if isinstance(data.get(timespan),list) else [data.get(timespan)] for timespan in self._timespan_list}
		else:
			self._avg = {timespan: [] for timespan in self._timespan_list}

		for key in self._avg.keys():
			if self._avg[key] == [None]:
				self._avg[key] = []

	def reset(self, data = None):
		for timespan in self._timespan_list:
			self._avg[timespan] = []

	def update(self, data):
		for timespan, value in data.items():
			if isinstance(value, int):
				self._avg[timespan].append(value)
			elif isinstance(value, list):
				self._avg[timespan].extend(value)

	def result(self):
		return collections.OrderedDict((timespan, self._avg[timespan]) for timespan in self._timespan_list)


class TimeSpanStats():
	def __init__(self, *, data = None, timespan = TimeSpan.DATE):
		self._items = {}
		self._timespan = timespan
		if timespan == TimeSpan.DATE:
			self._timespan_list = DATES
		elif timespan == TimeSpan.WEEKDAY:
			self._timespan_list = WEEKDAYS
		elif timespan == TimeSpan.WEEK:
			self._timespan_list = WEEKS
		elif timespan == TimeSpan.MONTH:
			self._timespan_list = MONTHS


		if isinstance(data, dict):
			self._items = {timespan: data.get(timespan) if isinstance(data.get(timespan),list) else [data.get(timespan)] for timespan in self._timespan_list}
		else:
			self._items = {timespan: [] for timespan in self._timespan_list}

		for key in self._items.keys():
			if self._items[key] == [None]:
				self._items[key] = []

	def reset(self, data = None):
		for timespan in self._timespan_list:
			self._items[timespan] = []

	def update(self, data):
		for timespan, value in data.items():
			try:
				if isinstance(value, collections.Iterable):
					self._items[timespan].extend(value)
				else:
					self._items[timespan].append(value)
			except Exception as e:
				print(e)

	def average(self, timespan=None):
		def get_average(data):
			try:
				return statistics.mean(data)
			except statistics.StatisticsError:
				return None

		if timespan is None:
			return collections.OrderedDict((timespan, get_average(self._items[timespan])) for timespan in self._timespan_list)
		else:
			try:
				return get_average(self._items[timespan])
			except KeyError:
				return None

	def median(self, timespan=None):
		def get_median(data):
			try:
				return statistics.median(data)
			except statistics.StatisticsError:
				return None

		if timespan is None:
			return collections.OrderedDict((timespan, get_median(self._items[timespan])) for timespan in self._timespan_list)
		else:
			try:
				return get_median(self._items[timespan])
			except KeyError:
				return None

	def stdev(self, timespan=None):
		def get_stdev(data):
			try:
				return statistics.stdev(data)
			except statistics.StatisticsError:
				return None

		if timespan is None:
			return collections.OrderedDict((timespan, get_stdev(self._items[timespan])) for timespan in self._timespan_list)
		else:
			try:
				return get_stdev(self._items[timespan])
			except KeyError:
				return None

	def items(self, timespan=None):
		if timespan is None:
			return collections.OrderedDict((timespan, self._items[timespan]) for timespan in self._timespan_list)
		else:
			try:
				return self._items[timespan]
			except KeyError:
				return None

	def __repr__(self):
		return  "Class: {}\n".format(self.__class__) + \
				"Timespan: {}\n".format(self._timespan) + \
				"Items: {}\n".format(self._items) + \
				"Average: {}\n".format(self.average()) + \
				"Median: {}\n".format(self.median()) + \
				"Stdev: {}".format(self.stdev())