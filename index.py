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
from dataprocessing.parse_file import process_file


# General
import argparse
import os
import sys
import logging

# Profiler
from guppy import hpy



processed_data = None

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




def main():
	global processed_data
	logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S", format="[%(asctime)s] - %(levelname)s - %(funcName)s ||| %(message)s")

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
