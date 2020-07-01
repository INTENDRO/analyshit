"""
app_common.py

Common layout chunks for all apps (navbar, etc.).
"""

import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(brand='Analyshit', brand_href='/', color='primary', dark=True,
children=[
	dbc.NavItem(dbc.NavLink("Home", href='/')),
	dbc.NavItem(dbc.NavLink("Debug", href='/debug')),
	dbc.NavItem(dbc.NavLink("Google", href='https://google.com'))

])