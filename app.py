import dash
import dash_bootstrap_components as dbc

####################################################################
# The following lines are required in order to get Bootstrap to run.
####################################################################

# <!-- CSS only -->
# <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">

# <!-- JS, Popper.js, and jQuery -->
# <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
# <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
# <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>



external_stylesheets = [
	"https://codepen.io/chriddyp/pen/bWLwgP.css",

	# Bootstrap
	{
		'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
		'rel': 'stylesheet',
		'integrity': 'sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk',
		'crossorigin': 'anonymous'
	},

	# Materialize
	# "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css"
]

external_scripts = [
	# Bootstrap
	{
		'src': 'https://code.jquery.com/jquery-3.5.1.slim.min.js',
		'integrity': 'sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj',
		'crossorigin': 'anonymous'
	},
	{
		'src': 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
		'integrity': 'sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo',
		'crossorigin': 'anonymous'
	},
	{
		'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js',
		'integrity': 'sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI',
		'crossorigin': 'anonymous'
	},

	# Materialize
	# "https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"
]


# Bootstrap is developed mobile-first. In order to support responsive rendering and touch zooming,
# this meta tag needs to be included:
# <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
# Meta tags can be added using a dictionary with the main Dash constructor

# does not work for some reason...
# meta_tags = {'name': 'viewport', 'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'}


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX]) #, meta_tags=meta_tags)