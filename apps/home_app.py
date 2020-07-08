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
			),

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
			),

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
		]),

		html.Div([
			dbc.Table([
				html.Thead(html.Tr([html.Th("Attribute"), html.Th("Count")])),
				html.Tbody([
					html.Tr([html.Td("Glück"), html.Td(processed_data["cnt_type"]["glück"])]),
					html.Tr([html.Td("Ninja"), html.Td(processed_data["cnt_type"]["ninja"])]),
					html.Tr([html.Td("Neocolor"), html.Td(processed_data["cnt_type"]["neocolor"])]),
					html.Tr([html.Td("Geiss"), html.Td(processed_data["cnt_type"]["geiss"])]),
					html.Tr([html.Td("Bier"), html.Td(processed_data["cnt_type"]["bier"])]),
				])
			],
			hover=True,
			striped=True,
			responsive=True)
		],
		style={'margin-left': '5vw', 'margin-right': '5vw', 'margin-top': 10, 'height':'80vh', 'width':'90vw'}
		)
	]




