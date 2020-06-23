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
		dcc.Textarea(
			id="debug-information",
			value="\n\n".join(map(lambda item: "{}:\n{}".format(item[0],item[1]),processed_data.items())),
			style={'width': '100%', 'height': 800},
		)
	]