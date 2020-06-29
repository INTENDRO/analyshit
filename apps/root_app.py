"""
root_app.py

This file is responsible for creating the layout for the main page.
All stats will be displayed on this page as tabs are used to 
switch between different categories instead of changing the page,
which would require another application.
"""

# Dash
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html


from app import app

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

		dcc.Link('View debug information', href='/debug'),
		
		html.H1(
			children='Analyshit',
			style={
				'textAlign': 'center',
				'fontSize': '64px'
			}
		),

		html.Div([
			html.Div([
				html.Div([
					" Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lacinia orci quam, sit amet posuere dolor ultricies vel. Aenean in sem dapibus metus dictum faucibus quis quis tortor. Vivamus vulputate elit vel maximus pellentesque. Quisque a diam dignissim, pulvinar mi eu, tempus sapien. Phasellus lectus diam, consectetur id est ac, fermentum tristique ipsum. Nam imperdiet metus erat, non tempor justo rhoncus id. Nam ullamcorper elit eget neque aliquam placerat. ",
					html.A(
						children="Go to google",
						href="https://google.com",
						className='btn btn-primary'
					)
				],
				className='card-body'
				),
			],
			className='card'
			),
		],
		className='container'
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

		dcc.Tabs([
			dcc.Tab(label='Weekday', children=[
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
				),
				dcc.Graph(
					id='avg-consistency-weekday-bar',
					figure={
						'data': [
							{
								'y': list(processed_data['consistency_stats_weekday'].average().values()),
								'type': 'bar'
							},
						],
						'layout': {
							'title': 'Average Consistency vs. Weekday',
							'xaxis': {
								'title': 'Weekday',
								'tickvals': [0,1,2,3,4,5,6],
								'ticktext': list(processed_data['consistency_stats_weekday'].average().keys())
							},
							'yaxis': {
								'title': 'Consistency',
								'tickvals': [1,2,3,4],
								'ticktext': ['d','w','n','h'],
								'range':[1,4]
							}
						}
					}
				),
				dcc.Graph(
					id='avg-size-weekday-bar',
					figure={
						'data': [
							{
								'y': list(processed_data['size_stats_weekday'].average().values()),
								'type': 'bar'
							},
						],
						'layout': {
							'title': 'Average Size vs. Weekday',
							'xaxis': {
								'title': 'Weekday',
								'tickvals': [0,1,2,3,4,5,6],
								'ticktext': list(processed_data['size_stats_weekday'].average().keys())
							},
							'yaxis': {
								'title': 'Size',
								'tickvals': [1,2,3],
								'ticktext': ['w','n','g'],
								'range':[1,3]
							}
						}
					}
				),
				dcc.Graph(
					id='avg-consistency-size-weekday-bar',
					figure={
						'data': [
							{
								'name': "Consistency",
								'y': list(processed_data['consistency_stats_weekday'].average().values()),
								'type': 'bar'
							},
							{
								'name': "Size",
								'y': list(processed_data['size_stats_weekday'].average().values()),
								'type': 'bar'
							}
						],
						'layout': {
							'title': 'Average Values vs. Weekday',
							'xaxis': {
								'title': 'Weekday',
								'tickvals': [0,1,2,3,4,5,6],
								'ticktext': list(processed_data['size_stats_weekday'].average().keys())
							},
							'yaxis': {
								'range':[1,4]
							}
						}
					}
				)
			]),
			dcc.Tab(label='Week', children=[
				dcc.Graph(
					id='avg-consistency-week-bar',
					figure={
						'data': [
							{
								'name': "Consistency",
								'x': list(processed_data['consistency_stats_week'].average().keys()),
								'y': list(processed_data['consistency_stats_week'].average().values()),
								'type': 'bar'
							}
						],
						'layout': {
							'title': 'Average Consistency vs. Week',
							'xaxis': {
								'title': 'Week',
							},
							'yaxis': {
								'range':[1,4]
							}
						}
					}
				),
				dcc.Graph(
					id='avg-size-week-bar',
					figure={
						'data': [
							{
								'name': "Size",
								'x': list(processed_data['size_stats_week'].average().keys()),
								'y': list(processed_data['size_stats_week'].average().values()),
								'type': 'bar'
							}
						],
						'layout': {
							'title': 'Average Size vs. Week',
							'xaxis': {
								'title': 'Week',
							},
							'yaxis': {
								'range':[1,3]
							}
						}
					}
				)
			]),
			dcc.Tab(label='Month', children = [
				dcc.Graph(
					id='avg-consistency-month-bar',
					figure={
						'data': [
							{
								'name': "Consistency",
								'x': list(processed_data['consistency_stats_month'].average().keys()),
								'y': list(processed_data['consistency_stats_month'].average().values()),
								'type': 'bar'
							}
						],
						'layout': {
							'title': 'Average Consistency vs. Month',
							'xaxis': {
								'title': 'Month',
							},
							'yaxis': {
								'range':[1,4]
							}
						}
					}
				),
				dcc.Graph(
					id='avg-size-month-bar',
					figure={
						'data': [
							{
								'name': "Size",
								'x': list(processed_data['size_stats_month'].average().keys()),
								'y': list(processed_data['size_stats_month'].average().values()),
								'type': 'bar'
							}
						],
						'layout': {
							'title': 'Average Size vs. Month',
							'xaxis': {
								'title': 'Month',
							},
							'yaxis': {
								'range':[1,3]
							}
						}
					}
				)
			])
		]),
	]




