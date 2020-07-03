"""
home_app.py

This file is responsible for creating the layout for the main page.
Average stats and heatmaps over the full year will be displayed on
this page.
"""

# Dash
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


from .app_common import navbar

import datetime
import logging




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
		if count is not None:
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

	return [
		dcc.Location(id='url', refresh=False),

		navbar,

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
					id='sittings-heatmap',
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
							title='Sittings Heatmap',
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
				id='consistency-heatmap',
				figure=dict(
					data=[
						dict(
							x=list(range(1,32)),
							y=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
							z=create_heatmap_matrix(processed_data['consistency_stats_date'].average()),
							xgap=1,
							ygap=1,
							colorscale='Reds',
							name='lksjdf',
							type='heatmap'
						)
					],
					layout=dict(
						title='Consistency Heatmap',
						yaxis=dict(
							autorange='reversed'
						)
					)
				)
			)
		],
		style={'backgroundColor':'#bbbbbb'}
		),

		html.Div([
			dcc.Graph(
				id='size-heatmap',
				figure=dict(
					data=[
						dict(
							x=list(range(1,32)),
							y=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
							z=create_heatmap_matrix(processed_data['size_stats_date'].average()),
							xgap=1,
							ygap=1,
							colorscale='Reds',
							name='lksjdf',
							type='heatmap'
						)
					],
					layout=dict(
						title='Size Heatmap',
						yaxis=dict(
							autorange='reversed'
						)
					)
				)
			)
		],
		style={'backgroundColor':'#bbbbbb'}
		),

		
	]




