from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

about_md_1 = dcc.Markdown(
'''
    TBD:
    * Data cleaning
    * Extra techniques used
    * ...
''',
id='about-extra'
)