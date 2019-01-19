import dash
from dash.dependencies import Input, Output
#from IPython.display import clear_output, Image, display
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
variable = 'temperature'
units = 'standard'
rcp = '6.5'
baseline = 'cru'
intermodal = 'off'

#app = dash.Dash('app', server=server)
app = dash.Dash(__name__)

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
    html.Button('Temperature', id='temperature'),
    html.Button('Precipitation', id='precipitation'),
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
            'y': dfhist.Temp - 32,
            'type': 'bar',
            'base': 32,
            'marker': {
                'color': '#999999'
            },
            'name': 'Historical'
        },{
            'x': df10s.Month,
            'y': df10s.Temp - 32,
            'type': 'bar',
            'base': 32,
            'marker': {
                'color': '#fecc5c'
            },
            'name': '2010-2019',
            'error_y': {
                'type': 'data',
                'array': df10s.Error,
                'visible': 'true'
            }
        },{
            'x': df40s.Month,
            'y': df40s.Temp - 32,
            'type': 'bar',
            'base': 32,
            'marker': {
                'color': '#fd8d3c'
            },
            'name': '2040-2049',
            'error_y': {
                'type': 'data',
                'array': df40s.Error,
                'visible': 'true'
            }
        },{
            'x': df60s.Month,
            'y': df60s.Temp - 32,
            'type': 'bar',
            'base': 32,
            'marker': {
                'color': '#f03b20'
            },
            'name': '2060-2069',
            'error_y': {
                'type': 'data',
                'array': df60s.Error,
                'visible': 'true'
            }
        },{
            'x': df90s.Month,
            'y': df90s.Temp - 32,
            'type': 'bar',
            'base': 32,
            'marker': {
                'color': '#bd0026'
            },
            'name': '2090-2099',
            'error_y': {
                'type': 'data',
                'array': df90s.Error,
                'visible': 'true'
            }
        }],
        'layout': {
            'barmode': 'grouped',
            'zeroline': 'false',
            'yaxis': {
                'zeroline': 'false',
            },
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            },
            'shapes': [{
                'type': 'line', 
                'x0': 0, 'x1': 1, 'xref': 'paper',
                'y0': 32, 'y1': 32, 'yref': 'y',
                'line': { 'width': 1 }
            }]
        }
    }
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run_server(debug=True, host='0.0.0.0', port=port)
