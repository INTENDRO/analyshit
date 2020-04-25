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
import logging

# Dash
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
	html.H1(children='Hello Dash'),

	html.Div(children='''
		Dash: A web application framework for Python.
	'''),

	dcc.Graph(
		id='example-graph',
		figure={
			'data': [
				{'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
				{'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
			],
			'layout': {
				'title': 'Mario Data Visualization'
			}
		}
	)
])

def parse_input_arguments():
	parser = argparse.ArgumentParser(description="Analyzing the defecational behavior over the span of one year.")
	parser.add_argument("-f", "--file", help="Specify the desired file.")
	args = parser.parse_args()
	return args

def get_project_directory():
	directory = os.path.dirname(os.path.realpath(__file__))
	logging.debug("home directory: {}".format(directory))
	return directory

def get_newest_filename():
	filename = sorted(os.listdir("./data"))[-1]
	logging.debug("newest file: {}".format(filename))
	return filename

def check_file_exists(file):
	if os.path.exists("./data/"+file):
		logging.debug("selected file exists")
		return True
	else:
		logging.error("selected file does not exist!")
		return False

def main():
	logging.basicConfig(level=logging.DEBUG, datefmt="%H:%M:%S", format="[%(asctime)s] - %(levelname)s - %(message)s")

	args = parse_input_arguments()
	home_dir = get_project_directory()
	if args.file:
		if not check_file_exists(args.file):
			logging.critical("Leaving the application...")
	else:
		filename = get_newest_filename()
		print(filename)

	app.run_server(debug=True)



if __name__ == "__main__":
	main()