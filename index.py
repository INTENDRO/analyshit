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
from apps import home_app, timespan_app, debug_app


# General
import argparse
import os
import sys
import logging
import re
import collections
import datetime



# Profiler
from guppy import hpy


from dataprocessing.timespan import TimeSpan, TimeSpanStats



app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])


@app.callback(	Output('page-content', 'children'),
				[Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/':
		return home_app.display_dash(processed_data)
	elif pathname == '/timespan':
		return timespan_app.display_dash(processed_data)
	elif pathname == '/debug':
		return debug_app.display_dash(processed_data)
	else:
		return '404'


processed_data = {}


CONSISTENCY_STR2NUM = {'d': 1, 'w': 2, 'n': 3, 'h': 4}
SIZE_STR2NUM = {'w': 1, 'n': 2, 'g': 3}



class OrderedCounter(collections.Counter, collections.OrderedDict):
	'Counter that remembers the order elements are first encountered'

	def __repr__(self):
		return '%s(%r)' % (self.__class__.__name__, collections.OrderedDict(self))

	def __reduce__(self):
		return self.__class__, (collections.OrderedDict(self),)







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
	global processed_data

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

	# return processed_data


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

	process_file(filepath)
	logging.debug("Keys of processed_data dict: {}".format(processed_data.keys()))


	print("\n\n")
	# display_dash(processed_data)
	# h = hpy()
	# print(h.heap())
	app.run_server(debug=True, host="0.0.0.0")



if __name__ == "__main__":
	main()