"""
timespan_app.py

This file is responsible for displaying various plots over different
timespans like weeks, months, etc.
"""

# Dash
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc


from .app_common import navbar

def display_dash(processed_data):
	return [
		dcc.Location(id='url', refresh=False),

		navbar,

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