import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

import flask
import pandas as pd
import time
import os

server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv')
df = pd.read_csv('communities.csv')

app = dash.Dash('app', server=server)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Community Charts'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Anchorage', 'value': 'Anchorage'},
            {'label': 'Fairbanks', 'value': 'Fairbanks'},
            {'label': 'Juneau', 'value': 'Juneau'}
        ],
        value='Anchorage'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])

def update_graph(selected_dropdown_value):
    dff = df[df['Community'] == selected_dropdown_value]
    dfhist = df[dff['Decades'] == '1961-1990']
    df10s = df[dff['Decades'] == '2010-2019']
    df40s = df[dff['Decades'] == '2090-2099']
    df60s = df[dff['Decades'] == '2060-2069']
    df90s = df[dff['Decades'] == '2090-2099']
    return {
        'data': [{
            'x': dfhist.Month,
            'y': dfhist.Temp,
            'type': 'bar',
            'marker': {
                'color': '#999999'
            },
            'name': 'Historical'
        },{
            'x': df10s.Month,
            'y': df10s.Temp,
            'type': 'bar',
            'marker': {
                'color': '#fecc5c'
            },
            'name': '2010-2019'
        },{
            'x': df40s.Month,
            'y': df40s.Temp,
            'type': 'bar',
            'marker': {
                'color': '#fd8d3c'
            },
            'name': '2040-2049'
        },{
            'x': df60s.Month,
            'y': df60s.Temp,
            'type': 'bar',
            'marker': {
                'color': '#f03b20'
            },
            'name': '2060-2069'
        },{
            'x': df90s.Month,
            'y': df90s.Temp,
            'type': 'bar',
            'marker': {
                'color': '#bd0026'
            },
            'name': '2090-2099'
        }],
        'layout': {
            'barmode': 'grouped',
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run_server(debug=True, host='0.0.0.0', port=port)
