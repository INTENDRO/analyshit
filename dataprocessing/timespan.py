import statistics
import collections
from enum import Enum
from .cont_average import ContAverage

MONTHS = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')
WEEKDAYS = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
DATES = (
	'200101',
	'200102',
	'200103',
	'200104',
	'200105',
	'200106',
	'200107',
	'200108',
	'200109',
	'200110',
	'200111',
	'200112',
	'200113',
	'200114',
	'200115',
	'200116',
	'200117',
	'200118',
	'200119',
	'200120',
	'200121',
	'200122',
	'200123',
	'200124',
	'200125',
	'200126',
	'200127',
	'200128',
	'200129',
	'200130',
	'200131',
	'200201',
	'200202',
	'200203',
	'200204',
	'200205',
	'200206',
	'200207',
	'200208',
	'200209',
	'200210',
	'200211',
	'200212',
	'200213',
	'200214',
	'200215',
	'200216',
	'200217',
	'200218',
	'200219',
	'200220',
	'200221',
	'200222',
	'200223',
	'200224',
	'200225',
	'200226',
	'200227',
	'200228',
	'200229',
	'200301',
	'200302',
	'200303',
	'200304',
	'200305',
	'200306',
	'200307',
	'200308',
	'200309',
	'200310',
	'200311',
	'200312',
	'200313',
	'200314',
	'200315',
	'200316',
	'200317',
	'200318',
	'200319',
	'200320',
	'200321',
	'200322',
	'200323',
	'200324',
	'200325',
	'200326',
	'200327',
	'200328',
	'200329',
	'200330',
	'200331',
	'200401',
	'200402',
	'200403',
	'200404',
	'200405',
	'200406',
	'200407',
	'200408',
	'200409',
	'200410',
	'200411',
	'200412',
	'200413',
	'200414',
	'200415',
	'200416',
	'200417',
	'200418',
	'200419',
	'200420',
	'200421',
	'200422',
	'200423',
	'200424',
	'200425',
	'200426',
	'200427',
	'200428',
	'200429',
	'200430',
	'200501',
	'200502',
	'200503',
	'200504',
	'200505',
	'200506',
	'200507',
	'200508',
	'200509',
	'200510',
	'200511',
	'200512',
	'200513',
	'200514',
	'200515',
	'200516',
	'200517',
	'200518',
	'200519',
	'200520',
	'200521',
	'200522',
	'200523',
	'200524',
	'200525',
	'200526',
	'200527',
	'200528',
	'200529',
	'200530',
	'200531',
	'200601',
	'200602',
	'200603',
	'200604',
	'200605',
	'200606',
	'200607',
	'200608',
	'200609',
	'200610',
	'200611',
	'200612',
	'200613',
	'200614',
	'200615',
	'200616',
	'200617',
	'200618',
	'200619',
	'200620',
	'200621',
	'200622',
	'200623',
	'200624',
	'200625',
	'200626',
	'200627',
	'200628',
	'200629',
	'200630',
	'200701',
	'200702',
	'200703',
	'200704',
	'200705',
	'200706',
	'200707',
	'200708',
	'200709',
	'200710',
	'200711',
	'200712',
	'200713',
	'200714',
	'200715',
	'200716',
	'200717',
	'200718',
	'200719',
	'200720',
	'200721',
	'200722',
	'200723',
	'200724',
	'200725',
	'200726',
	'200727',
	'200728',
	'200729',
	'200730',
	'200731',
	'200801',
	'200802',
	'200803',
	'200804',
	'200805',
	'200806',
	'200807',
	'200808',
	'200809',
	'200810',
	'200811',
	'200812',
	'200813',
	'200814',
	'200815',
	'200816',
	'200817',
	'200818',
	'200819',
	'200820',
	'200821',
	'200822',
	'200823',
	'200824',
	'200825',
	'200826',
	'200827',
	'200828',
	'200829',
	'200830',
	'200831',
	'200901',
	'200902',
	'200903',
	'200904',
	'200905',
	'200906',
	'200907',
	'200908',
	'200909',
	'200910',
	'200911',
	'200912',
	'200913',
	'200914',
	'200915',
	'200916',
	'200917',
	'200918',
	'200919',
	'200920',
	'200921',
	'200922',
	'200923',
	'200924',
	'200925',
	'200926',
	'200927',
	'200928',
	'200929',
	'200930',
	'201001',
	'201002',
	'201003',
	'201004',
	'201005',
	'201006',
	'201007',
	'201008',
	'201009',
	'201010',
	'201011',
	'201012',
	'201013',
	'201014',
	'201015',
	'201016',
	'201017',
	'201018',
	'201019',
	'201020',
	'201021',
	'201022',
	'201023',
	'201024',
	'201025',
	'201026',
	'201027',
	'201028',
	'201029',
	'201030',
	'201031',
	'201101',
	'201102',
	'201103',
	'201104',
	'201105',
	'201106',
	'201107',
	'201108',
	'201109',
	'201110',
	'201111',
	'201112',
	'201113',
	'201114',
	'201115',
	'201116',
	'201117',
	'201118',
	'201119',
	'201120',
	'201121',
	'201122',
	'201123',
	'201124',
	'201125',
	'201126',
	'201127',
	'201128',
	'201129',
	'201130',
	'201201',
	'201202',
	'201203',
	'201204',
	'201205',
	'201206',
	'201207',
	'201208',
	'201209',
	'201210',
	'201211',
	'201212',
	'201213',
	'201214',
	'201215',
	'201216',
	'201217',
	'201218',
	'201219',
	'201220',
	'201221',
	'201222',
	'201223',
	'201224',
	'201225',
	'201226',
	'201227',
	'201228',
	'201229',
	'201230',
	'201231'
)


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
			self._timespan_list = list(range(1,54))
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
			self._timespan_list = list(range(1,54))
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
			self._timespan_list = list(range(1,54))
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