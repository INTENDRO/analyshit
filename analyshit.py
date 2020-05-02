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

# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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

	html.Div([
		html.Label("Avg. Consistency:", style=avg_count_style),
		html.Label("Avg. Size:", style=avg_count_style),
		html.Label("Glück Count:", style=avg_count_style),
		html.Label("Ninja Count:", style=avg_count_style),
		html.Label("Neocolor Count:", style=avg_count_style),
		html.Label("Geiss Count:", style=avg_count_style),
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
							z=[
								[1,2,3],
								[3,2,1],
								[2,2,2]
							],
							colorscale='Reds',
							name='lksjdf',
							type='heatmap'
						)
					],
					layout=dict(
						title='Calendar Heatmap'
					)
				)
			)
		],
		style={'backgroundColor':'#bbbbbb', 'width': '50%', 'float':'right', 'height': '100%'}
		)
	],
	style={'columnCount':1, 'backgroundColor':'#111111'}
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
				entry["consistency"] = match.group(4)
				entry["size"] = match.group(5)
				entry["type"] = match.group(6)
				yield entry
			else:
				logging.warning("could not parse line: {}".format(line))
			



def process_file(filepath):
	logging.debug("processing file {}".format(filepath))

	for entry in parse_line(filepath):
		print(entry)






def main():
	logging.basicConfig(level=logging.DEBUG, datefmt="%H:%M:%S", format="[%(asctime)s] - %(levelname)s - %(funcName)s ||| %(message)s")

	args = parse_input_arguments()
	home_dir = get_project_directory()
	data_dir = os.path.join(home_dir,"data")
	logging.debug("home_dir: {}".format(home_dir))
	logging.debug("data_dir: {}".format(data_dir))

	if args.file:
		# if not check_file_exists(args.file):
		# 	logging.critical("Leaving the application...")
		# 	sys.exit(-1)
		# else:
		# 	filename = args.file
		# 	logging.debug("file {} exists!".format(filename))
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


	print("\n\n")
	app.run_server(debug=True, host="0.0.0.0")



if __name__ == "__main__":
	main()