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
							x=[1,2,3,4,5],
							y=[4,2,3,4,2],
							name='Test Graph'
						),
						dict(
							x=[1,2,3,4,5],
							y=[5,3,5,1,3],
							name='lksjdf'
						),
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


	print("\n\n")
	app.run_server(debug=True, host="0.0.0.0")



if __name__ == "__main__":
	main()