# Dash
import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html


from app import app



def display_dash(processed_data):
	return [
		dcc.Location(id='url', refresh=False),
		dcc.Link('Go to main page', href='/'),
		html.Br(),
		html.Textarea("\n".join([
					"average_consistency: {}".format(processed_data['average_consistency']),
					"average_size: {}".format(processed_data['average_size']),
					"cnt_sittings_weekday: {}".format(processed_data['cnt_sittings_weekday']),
					"cnt_consistency: {}".format(processed_data['cnt_consistency']),
					"cnt_size: {}".format(processed_data['cnt_size']),
					"cnt_type: {}".format(processed_data['cnt_type']),
					"cnt_sittings_date: {}".format(processed_data['cnt_sittings_date']),
					"consistency_stats_month:\n{}\n".format(processed_data['consistency_stats_month']),
					"size_stats_month:\n{}\n".format(processed_data['size_stats_month']),
					"consistency_stats_week:\n{}\n".format(processed_data['consistency_stats_week']),
					"size_stats_week:\n{}\n".format(processed_data['size_stats_week']),
					"consistency_stats_weekday:\n{}\n".format(processed_data['consistency_stats_weekday']),
					"size_stats_weekday:\n{}\n".format(processed_data['size_stats_weekday']),
					# "consistency_stats_date:\n{}\n".format(processed_data['consistency_stats_date']),
					# "size_stats_date:\n{}\n".format(processed_data['size_stats_date']),
				]),
				cols= 100,
				rows=50
			)
	]