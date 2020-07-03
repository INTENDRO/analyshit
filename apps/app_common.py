"""
app_common.py

Common layout chunks for all apps (navbar, etc.).
"""

import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(brand='Analyshit', brand_href='/', brand_style={'font-size':'200%'}, color='primary', dark=True, style={'font-size': '150%'},
children=[
	dbc.NavItem(dbc.NavLink("Home", href='/')),
	dbc.NavItem(dbc.NavLink("Debug", href='/debug'))

])