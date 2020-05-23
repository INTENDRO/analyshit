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



external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
WEEKDAYS = ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')
CONSISTENCY_STR2NUM = {'d': 1, 'w': 2, 'n': 3, 'h': 4}
SIZE_STR2NUM = {'w': 1, 'n': 2, 'g': 3}

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


class WeekdayAverage():
	def __init__(self, data = None):
		self._avg = {}

		if isinstance(data, dict):
			self._avg = {weekday: ContAverage(data.get(weekday)) for weekday in WEEKDAYS}
		else:
			self._avg = {weekday: ContAverage() for weekday in WEEKDAYS}

	def reset(self, data = None):
		for weekday in WEEKDAYS:
			self._avg[weekday].reset()

	def update(self, data):
		for weekday, value in data.items():
			self._avg[weekday].update(value)

	def result(self):
		return collections.OrderedDict((weekday, self._avg[weekday].result()) for weekday in WEEKDAYS)



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
					"cnt_sittings_weekday: {}".format(processed_data['cnt_sittings_weekday']),
					"cnt_consistency: {}".format(processed_data['cnt_consistency']),
					"cnt_size: {}".format(processed_data['cnt_size']),
					"cnt_type: {}".format(processed_data['cnt_type']),
					"cnt_sittings_date: {}".format(processed_data['cnt_sittings_date']),
					"avg_consistency_weekday: {}".format(processed_data['avg_consistency_weekday']),
					"avg_size_weekday: {}".format(processed_data['avg_size_weekday'])
				]),
				cols= 100,
				rows=80
			)
		),

		html.Div([
			html.Label("Avg. Consistency: {:.3f}".format(processed_data["average_consistency"]), style=avg_count_style),
			html.Label("Avg. Size: {:.3f}".format(processed_data["average_size"]), style=avg_count_style),
			html.Label("Glück Count: {}".format(processed_data["cnt_type"]["glück"]), style=avg_count_style),
			html.Label("Ninja Count: {}".format(processed_data["cnt_type"]["ninja"]), style=avg_count_style),
			html.Label("Neocolor Count: {}".format(processed_data["cnt_type"]["neocolor"]), style=avg_count_style),
			html.Label("Geiss Count: {}".format(processed_data["cnt_type"]["geiss"]), style=avg_count_style),
			html.Label("Bier Count: {}".format(processed_data["cnt_type"]["bier"]), style=avg_count_style), 
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
								z=create_heatmap_matrix(processed_data['cnt_sittings_date']),
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
							'y': list(processed_data['cnt_sittings_weekday'].values()),
							'type': 'bar'
						},
					],
					'layout': {
						'title': 'Amount of Individual Sittings per Weekday',
						'xaxis': {
							'title': 'Weekday',
							'tickvals': [0,1,2,3,4,5,6],
							'ticktext': list(processed_data['cnt_sittings_weekday'].keys())
						}
					}
				}
			)
		],
		style={'backgroundColor':'#eeeeee'}
		),

		html.Div([
			dcc.Graph(
				id='avg-consistency-weekday-bar',
				figure={
					'data': [
						{
							'y': list(processed_data['avg_consistency_weekday'].values()),
							'type': 'bar'
						},
					],
					'layout': {
						'title': 'Average Consistency vs. Weekday',
						'xaxis': {
							'title': 'Weekday',
							'tickvals': [0,1,2,3,4,5,6],
							'ticktext': list(processed_data['avg_consistency_weekday'].keys())
						},
						'yaxis': {
							'title': 'Consistency',
							'tickvals': [1,2,3,4],
							'ticktext': ['d','w','n','h'],
							'range':[1,4]
						}
					}
				}
			)
		],
		style={'backgroundColor':'#eeeeee'}
		),

		html.Div([
			dcc.Graph(
				id='avg-size-weekday-bar',
				figure={
					'data': [
						{
							'y': list(processed_data['avg_size_weekday'].values()),
							'type': 'bar'
						},
					],
					'layout': {
						'title': 'Average Size vs. Weekday',
						'xaxis': {
							'title': 'Weekday',
							'tickvals': [0,1,2,3,4,5,6],
							'ticktext': list(processed_data['avg_size_weekday'].keys())
						},
						'yaxis': {
							'title': 'Size',
							'tickvals': [1,2,3],
							'ticktext': ['w','n','g'],
							'range':[1,3]
						}
					}
				}
			)
		],
		style={'backgroundColor':'#eeeeee'}
		),

		html.Div([
			dcc.Graph(
				id='avg-consistency-size-weekday-bar',
				figure={
					'data': [
						{
							'name': "Consistency",
							'y': list(processed_data['avg_consistency_weekday'].values()),
							'type': 'bar'
						},
						{
							'name': "Size",
							'y': list(processed_data['avg_size_weekday'].values()),
							'type': 'bar'
						}
					],
					'layout': {
						'title': 'Average Values vs. Weekday',
						'xaxis': {
							'title': 'Weekday',
							'tickvals': [0,1,2,3,4,5,6],
							'ticktext': list(processed_data['avg_size_weekday'].keys())
						},
						'yaxis': {
							'range':[1,4]
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
	cnt_sittings_date = OrderedCounter()
	cnt_sittings_weekday = collections.Counter()
	cnt_consistency = collections.Counter()
	cnt_size = collections.Counter()
	cnt_type = collections.Counter()

	# weekday stats
	avg_consistency_weekday = WeekdayAverage()
	avg_size_weekday = WeekdayAverage()

	for entry in parse_line(filepath):
		cnt_sittings_date.update([entry["date"]])
		cnt_sittings_weekday.update([entry["weekday"]])
		cnt_consistency.update(entry["consistency"])
		cnt_size.update(entry["size"])
		cnt_type.update([entry["type"]])

		consistency_value = CONSISTENCY_STR2NUM[entry["consistency"]]
		size_value = SIZE_STR2NUM[entry["size"]]

		avg_consistency_weekday.update({entry["weekday"]: consistency_value})
		avg_size_weekday.update({entry["weekday"]: size_value})


	# convert the weekday counter to an ordered counter using the conventional order of weekdays starting on monday
	cnt_sittings_weekday = OrderedCounter({k:cnt_sittings_weekday[k] for k in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun')})

	logging.debug("cnt_sittings_weekday: {}".format(cnt_sittings_weekday))
	logging.debug("cnt_consistency: {}".format(cnt_consistency))
	logging.debug("cnt_size: {}".format(cnt_size))
	logging.debug("cnt_type: {}".format(cnt_type))
	logging.debug("cnt_sittings_date: {}".format(cnt_sittings_date))
	logging.debug("avg_consistency_weekday: {}".format(avg_consistency_weekday.result()))
	logging.debug("avg_size_weekday: {}".format(avg_size_weekday.result()))


	processed_data["cnt_type"] = cnt_type
	processed_data["cnt_size"] = cnt_size
	processed_data["cnt_consistency"] = cnt_consistency
	processed_data["cnt_sittings_weekday"] = cnt_sittings_weekday
	processed_data["cnt_sittings_date"] = cnt_sittings_date
	processed_data["avg_consistency_weekday"] = avg_consistency_weekday.result()
	processed_data["avg_size_weekday"] = avg_size_weekday.result()



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
	display_dash(processed_data)
	app.run_server(debug=True, host="0.0.0.0")



if __name__ == "__main__":
	main()