"""
Analyshit

Analyzing the defecational behavior over the span of one year.

Diagrams and Outputs:
- Average values (consistency, size)
- Counts (glück, ninja, etc.)
- Heat Map (consistency, size)
- Average values on Weekdays (consistency, size)


To Do:
- Convert DATES constants list to generator (safe memory)
- refactor TimeSpanList constructor
"""

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app
from apps import app1


# General
import argparse
import os
import sys
import logging
import re
import collections
import datetime
import statistics
from enum import Enum


# Profiler
from guppy import hpy




app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])


@app.callback(	Output('page-content', 'children'),
				[Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/apps/app1':
		return app1.layout
	else:
		return '404'



CONSISTENCY_STR2NUM = {'d': 1, 'w': 2, 'n': 3, 'h': 4}
SIZE_STR2NUM = {'w': 1, 'n': 2, 'g': 3}

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

class OrderedCounter(collections.Counter, collections.OrderedDict):
	'Counter that remembers the order elements are first encountered'

	def __repr__(self):
		return '%s(%r)' % (self.__class__.__name__, collections.OrderedDict(self))

	def __reduce__(self):
		return self.__class__, (collections.OrderedDict(self),)


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


def parse_input_arguments():
	parser = argparse.ArgumentParser(description="Analyzing the defecational behavior over the span of one year.")
	parser.add_argument("-f", "--file", help="Specify the desired file.")
	args = parser.parse_args()
	return args

def get_project_directory():
	directory = os.path.dirname(os.path.realpath(__file__))
	return directory

def get_newest_filename(data_dir):
	filename = sorted(os.listdir(data_dir))[-1]
	return filename

def check_file_exists(filepath):
	return os.path.exists(filepath)


def parse_line(filepath):
	regex = re.compile("(\d{2}).(\d{2}).(\d{2})\s+([hnwd])\s+([gnw])\s*(ninja|glück|geiss|bier|neocolor)?")
	with open(filepath,'r') as f:
		for line in f:
			match = regex.search(line)
			if match:
				entry = {}
				date = datetime.date(2000 + int(match.group(3)),int(match.group(2)),int(match.group(1)))
				entry["day"] = match.group(1)
				entry["month"] = match.group(2)
				entry["year"] = match.group(3)
				entry["date"] = match.group(3)+match.group(2)+match.group(1)
				entry["month_str"] = date.strftime("%b")
				entry["weekday"] = date.strftime("%a")
				entry["weeknum"] = date.isocalendar()[1]
				entry["consistency"] = match.group(4)
				entry["size"] = match.group(5)
				entry["type"] = match.group(6)
				yield entry
			else:
				logging.warning("could not parse line: {}".format(line))
			



def process_file(filepath):
	logging.debug("processing file {}".format(filepath))
	processed_data = {}


	# counts
	cnt_sittings_date = OrderedCounter()
	cnt_sittings_weekday = collections.Counter()
	cnt_consistency = collections.Counter()
	cnt_size = collections.Counter()
	cnt_type = collections.Counter()

	# month stats
	consistency_stats_month = TimeSpanStats(timespan = TimeSpan.MONTH)
	size_stats_month = TimeSpanStats(timespan = TimeSpan.MONTH)

	# week stats
	consistency_stats_week = TimeSpanStats(timespan = TimeSpan.WEEK)
	size_stats_week = TimeSpanStats(timespan = TimeSpan.WEEK)

	# weekday stats
	consistency_stats_weekday = TimeSpanStats(timespan = TimeSpan.WEEKDAY)
	size_stats_weekday = TimeSpanStats(timespan = TimeSpan.WEEKDAY)

	# date stats
	consistency_stats_date = TimeSpanStats(timespan = TimeSpan.DATE)
	size_stats_date = TimeSpanStats(timespan = TimeSpan.DATE)


	for entry in parse_line(filepath):
		cnt_sittings_date.update([entry["date"]])
		cnt_sittings_weekday.update([entry["weekday"]])
		cnt_consistency.update(entry["consistency"])
		cnt_size.update(entry["size"])
		cnt_type.update([entry["type"]])

		consistency_value = CONSISTENCY_STR2NUM[entry["consistency"]]
		size_value = SIZE_STR2NUM[entry["size"]]

		consistency_stats_month.update({entry["month_str"]: consistency_value})
		size_stats_month.update({entry["month_str"]: size_value})

		consistency_stats_week.update({entry["weeknum"]: consistency_value})
		size_stats_week.update({entry["weeknum"]: size_value})

		consistency_stats_weekday.update({entry["weekday"]: consistency_value})
		size_stats_weekday.update({entry["weekday"]: size_value})

		consistency_stats_date.update({entry["date"]: consistency_value})
		size_stats_date.update({entry["date"]: size_value})


	# convert the weekday counter to an ordered counter using the conventional order of weekdays starting on monday
	cnt_sittings_weekday = OrderedCounter({k:cnt_sittings_weekday[k] for k in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')})

	logging.debug("cnt_sittings_weekday: {}".format(cnt_sittings_weekday))
	logging.debug("cnt_consistency: {}".format(cnt_consistency))
	logging.debug("cnt_size: {}".format(cnt_size))
	logging.debug("cnt_type: {}".format(cnt_type))
	logging.debug("cnt_sittings_date: {}".format(cnt_sittings_date))
	logging.debug("consistency_stats_month:\n{}\n".format(consistency_stats_month))
	logging.debug("size_stats_month:\n{}\n".format(size_stats_month))
	logging.debug("consistency_stats_week:\n{}\n".format(consistency_stats_week))
	logging.debug("size_stats_week:\n{}\n".format(size_stats_week))
	logging.debug("consistency_stats_weekday:\n{}\n".format(consistency_stats_weekday))
	logging.debug("size_stats_weekday:\n{}\n".format(size_stats_weekday))
	logging.debug("consistency_stats_date:\n{}\n".format(consistency_stats_date))
	logging.debug("size_stats_date:\n{}\n".format(size_stats_date))


	processed_data["cnt_type"] = cnt_type
	processed_data["cnt_size"] = cnt_size
	processed_data["cnt_consistency"] = cnt_consistency
	processed_data["cnt_sittings_weekday"] = cnt_sittings_weekday
	processed_data["cnt_sittings_date"] = cnt_sittings_date
	processed_data["consistency_stats_month"] = consistency_stats_month
	processed_data["size_stats_month"] = size_stats_month
	processed_data["consistency_stats_week"] = consistency_stats_week
	processed_data["size_stats_week"] = size_stats_week
	processed_data["consistency_stats_weekday"] = consistency_stats_weekday
	processed_data["size_stats_weekday"] = size_stats_weekday
	processed_data["consistency_stats_date"] = consistency_stats_date
	processed_data["size_stats_date"] = size_stats_date



	# average consistency
	avg_const = (1*cnt_consistency["d"] + 2*cnt_consistency["w"] + 3*cnt_consistency["n"] + 4*cnt_consistency["h"]) / sum(cnt_consistency.values())
	logging.debug("avg. consistency: {}".format(avg_const))

	processed_data["average_consistency"] = avg_const

	# average size
	avg_size = (1*cnt_size["w"] + 2*cnt_size["n"] + 3*cnt_size["g"]) / sum(cnt_size.values())
	logging.debug("avg. size: {}".format(avg_size))

	processed_data["average_size"] = avg_size

	return processed_data


def main():
	logging.basicConfig(level=logging.DEBUG, datefmt="%H:%M:%S", format="[%(asctime)s] - %(levelname)s - %(funcName)s ||| %(message)s")

	args = parse_input_arguments()
	home_dir = get_project_directory()
	data_dir = os.path.join(home_dir,"data")
	logging.debug("home_dir: {}".format(home_dir))
	logging.debug("data_dir: {}".format(data_dir))

	if args.file:
		filename = args.file
		logging.debug("selected file: {}".format(filename))

	else:
		filename = get_newest_filename(data_dir)
		logging.debug("getting newest file: {}".format(filename))

	filepath = os.path.join(data_dir,filename)
	logging.debug("absolute filepath: {}".format(filepath))
	if not check_file_exists(filepath):
		logging.error("File does not exist!")
		logging.critical("Leaving the application...")
		sys.exit(-1)
	logging.debug("file exists!")

	processed_data = process_file(filepath)
	logging.debug("Keys of processed_data dict: {}".format(processed_data.keys()))


	print("\n\n")
	# display_dash(processed_data)
	# h = hpy()
	# print(h.heap())
	app.run_server(debug=True, host="0.0.0.0")



if __name__ == "__main__":
	main()