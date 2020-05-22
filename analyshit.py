"""
Analyshit

Analyzing the defecational behavior over the span of one year.

Diagrams and Outputs:
- Average values (consistency, size)
- Counts (glück, ninja, etc.)
- Heat Map (consistency, size)
- Average values on Weekdays (consistency, size)


"""

# General
import argparse
import os
import sys
import logging
import re
import collections
import datetime

# Dash
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html


class OrderedCounter(collections.Counter, collections.OrderedDict):
	'Counter that remembers the order elements are first encountered'

	def __repr__(self):
		return '%s(%r)' % (self.__class__.__name__, collections.OrderedDict(self))

	def __reduce__(self):
		return self.__class__, (collections.OrderedDict(self),)


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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
 


def create_heatmap_matrix(dataset):
	"""
	Why not [[0]*31]*12 ?
	The inner multiplication operator creates a list with every element
	containing a reference to the number '0'. If an element is changed later,
	the reference is updated to the new number. The outer multiplication 
	operator creates another list with references to the inner list. If a number
	in the inner list is changed, the list containing this number is modified
	and its reference does not change because lists are mutable. As the outer
	list is made up of the same references to this list, all the lists contained
	in the outer list are changed.

	The key to this is mutability. Multiplying the number for the inner list
	works because integers are immutable. Multiplying the lists for the outer
	list does not work as intended as the lists are mutable.
	"""
	heatmap_matrix = [[0]*31 for x in range(12)]

	for (date,count) in dataset.items():
		date = datetime.date(2000 + int(date[0:2]),int(date[2:4]),int(date[4:6]))
		# date.month contains the needed month index [1-12]
		# date.day contains the needed day index [1-(however long the month is)]

		heatmap_matrix[date.month-1][date.day-1] = count

	logging.debug("create_heatmap_matrix output: {}".format(heatmap_matrix))

	return heatmap_matrix


def display_dash(processed_data):
	avg_count_style = {
		'textAlign': 'center',
		'fontSize': '24px'
	}

	weekday_style = {
		'fontSize': '24px',
	}

	app.layout = html.Div([
		html.H1(
			children='Analyshit',
			style={
				'textAlign': 'center',
				'fontSize': '64px'
			}
		),
		html.Div(
			html.Textarea("\n".join([
					"average_consistency: {}".format(processed_data['average_consistency']),
					"average_size: {}".format(processed_data['average_size']),
					"weekday_counter: {}".format(processed_data['weekday_counter']),
					"consistency_counter: {}".format(processed_data['consistency_counter']),
					"size_counter: {}".format(processed_data['size_counter']),
					"type_counter: {}".format(processed_data['type_counter']),
					"date_counter: {}".format(processed_data['date_counter']),
					"keys: {}".format(processed_data['weekday_counter'].keys()),
					"values: {}".format(processed_data['weekday_counter'].values()),
					"items: {}".format(processed_data['weekday_counter'].items())
				]),
				cols= 100,
				rows=80
			)
		),

		html.Div([
			html.Label("Avg. Consistency: {:.3f}".format(processed_data["average_consistency"]), style=avg_count_style),
			html.Label("Avg. Size: {:.3f}".format(processed_data["average_size"]), style=avg_count_style),
			html.Label("Glück Count: {}".format(processed_data["type_counter"]["glück"]), style=avg_count_style),
			html.Label("Ninja Count: {}".format(processed_data["type_counter"]["ninja"]), style=avg_count_style),
			html.Label("Neocolor Count: {}".format(processed_data["type_counter"]["neocolor"]), style=avg_count_style),
			html.Label("Geiss Count: {}".format(processed_data["type_counter"]["geiss"]), style=avg_count_style),
			html.Label("Bier Count: {}".format(processed_data["type_counter"]["bier"]), style=avg_count_style), 
		],
		style={'columnCount':2, 'backgroundColor':'#eeeeee'}
		),

		html.Div([
			html.Div([
				html.Label("Monday", style=weekday_style),
				html.Label("Tuesday", style=weekday_style),
				html.Label("Wednesday", style=weekday_style),
			],
			style={'columnCount':'1' ,'backgroundColor':'#dddddd', 'width': '50%', 'float':'left'}
			),
			html.Div([
				dcc.Graph(
					id='calendar-heatmap',
					figure=dict(
						data=[
							dict(
								x=list(range(1,32)),
								y=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
								z=create_heatmap_matrix(processed_data['date_counter']),
								xgap=1,
								ygap=1,
								colorscale='Reds',
								name='lksjdf',
								type='heatmap'
							)
						],
						layout=dict(
							title='Calendar Heatmap',
							yaxis=dict(
								autorange='reversed'
							)
						)
					)
				)
			],
			style={'backgroundColor':'#bbbbbb', 'width': '50%', 'float':'right', 'height': '100%'}
			)
		],
		style={'columnCount':1, 'backgroundColor':'#111111'}
		),

		html.Div([
			daq.Gauge(
				id='consistency-gauge',
				label='Average Consistency',
				min=1,
				max=4,
				showCurrentValue=True,
				scale={'custom':{1:{'label':'d'}, 2:{'label':'w'}, 3:{'label':'n'}, 4:{'label':'h'}}},
				value=processed_data["average_consistency"]
			),
			daq.Gauge(
				id='size-gauge',
				label='Average Size',
				min=1,
				max=3,
				showCurrentValue=True,
				scale={'custom':{1:{'label':'w'}, 2:{'label':'n'}, 3:{'label':'g'}}},
				value=processed_data["average_size"],
			)  
		],
		style={'columnCount':2, 'backgroundColor':'#ffffff'}
		),

		html.Div([
			dcc.Graph(
				id='weekday-count-bar',
				figure={
					'data': [
						{
							'y': list(processed_data['weekday_counter'].values()),
							'type': 'bar'
						},
					],
					'layout': {
						'title': 'Amount of Individual Sittings per Weekday',
						'xaxis': {
							'title': 'Weekday',
							'tickvals': [0,1,2,3,4,5,6],
							'ticktext': list(processed_data['weekday_counter'].keys())
						}
					}
				}
			)
		],
		style={'backgroundColor':'#eeeeee'}
		)
	])

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
				entry["day"] = match.group(1)
				entry["month"] = match.group(2)
				entry["year"] = match.group(3)
				entry["date"] = match.group(3)+match.group(2)+match.group(1)
				entry["weekday"] = datetime.date(2000 + int(match.group(3)),int(match.group(2)),int(match.group(1))).strftime("%a")
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
	date_counter = OrderedCounter()
	weekday_counter = collections.Counter()
	consistency_counter = collections.Counter()
	size_counter = collections.Counter()
	type_counter = collections.Counter()

	# weekday stats
	avg_size_weekday = ContAverage([10]*3)

	logging.debug(type(avg_size_weekday))
	logging.debug(avg_size_weekday.current_sum())
	logging.debug(avg_size_weekday.current_count())
	logging.debug(avg_size_weekday.result())
	avg_size_weekday.update(20)
	logging.debug(avg_size_weekday.current_sum())
	logging.debug(avg_size_weekday.current_count())
	logging.debug(avg_size_weekday.result())
	avg_size_weekday.update([100,200,300])
	logging.debug(avg_size_weekday.current_sum())
	logging.debug(avg_size_weekday.current_count())
	logging.debug(avg_size_weekday.result())

	for entry in parse_line(filepath):
		date_counter.update([entry["date"]])
		weekday_counter.update([entry["weekday"]])
		consistency_counter.update(entry["consistency"])
		size_counter.update(entry["size"])
		type_counter.update([entry["type"]])

	# convert the weekday counter to an ordered counter using the conventional order of weekdays starting on monday
	weekday_counter = OrderedCounter({k:weekday_counter[k] for k in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')})

	logging.debug("weekday_counter: {}".format(weekday_counter))
	logging.debug("consistency_counter: {}".format(consistency_counter))
	logging.debug("size_counter: {}".format(size_counter))
	logging.debug("type_counter: {}".format(type_counter))
	logging.debug("date_counter: {}".format(date_counter))


	processed_data["type_counter"] = type_counter
	processed_data["size_counter"] = size_counter
	processed_data["consistency_counter"] = consistency_counter
	processed_data["weekday_counter"] = weekday_counter
	processed_data["date_counter"] = date_counter


	# average consistency
	avg_const = (1*consistency_counter["d"] + 2*consistency_counter["w"] + 3*consistency_counter["n"] + 4*consistency_counter["h"]) / sum(consistency_counter.values())
	logging.debug("avg. consistency: {}".format(avg_const))

	processed_data["average_consistency"] = avg_const

	# average size
	avg_size = (1*size_counter["w"] + 2*size_counter["n"] + 3*size_counter["g"]) / sum(size_counter.values())
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
	display_dash(processed_data)
	app.run_server(debug=True, host="0.0.0.0")



if __name__ == "__main__":
	main()