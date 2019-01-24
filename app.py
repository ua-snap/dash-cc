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
units = 'imperial'
variability = True

#app = dash.Dash('app', server=server)
app = dash.Dash(__name__)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Community Charts'),
    dcc.Dropdown(
        id='community',
        options=[
            {'label': 'Anchorage', 'value': 'Anchorage'},
            {'label': 'Fairbanks', 'value': 'Fairbanks'},
            {'label': 'Juneau', 'value': 'Juneau'}
        ],
        value='Anchorage'
    ),
    html.Label('Temperature or precipitation?'),
    dcc.RadioItems(
        options=[
            {'label': 'Temperature', 'value': 'temp'},
            {'label': 'Precipitation', 'value': 'precip'}
        ],
        id='variable',
        value='temp'
    ),
    html.Label('Units'),
    dcc.RadioItems(
        options=[
            {'label': 'Imperial', 'value': 'imperial'},
            {'label': 'Metric', 'value': 'metric'}
        ],
        id='units',
        value='imperial'
    ),
    html.Label('Scenario'),
    dcc.RadioItems(
        options=[
            {'label': 'RCP4.5', 'value': 'rcp45'},
            {'label': 'RCP6.0', 'value': 'rcp60'},
            {'label': 'RCP8.5', 'value': 'rcp85'}
        ],
        id='scenario',
        value='rcp60'
    ),
    html.Label('Historical Baseline'),
    dcc.RadioItems(
        options=[
            {'label': 'CRU', 'value': 'cru'},
            {'label': 'PRISM', 'value': 'prism'}
        ],
        id='baseline',
        value='cru'
    ),
    html.Label('Intermodel Variability'),
    dcc.RadioItems(
        options=[
            {'label': 'On', 'value': 'on'},
            {'label': 'Off', 'value': 'off'}
        ],
        id='variability',
        value='off'
    ),
    dcc.Graph(id='ccharts')
], className="container")

@app.callback(
    Output('ccharts', 'figure'),
    inputs=[
        Input('community', 'value'),
        Input('variable', 'value'),
        Input('scenario', 'value'),
        Input('variability', 'value')
    ]
)
def update_graph(community, variable, scenario, variability):
    """ Update the graph from user input """

    variability = variability == 'on'  # convert to boolean for use in configuring graph

    dff = df[df['Community'] == community]
    df0 = dff[dff['Scenario'] == scenario]

    dfhist = dff[dff['Decades'] == '1961-1990']
    df10s = df0[dff['Decades'] == '2010-2019']
    df40s = df0[dff['Decades'] == '2090-2099']  # ??? those are not the 40s :)
    df60s = df0[dff['Decades'] == '2060-2069']
    df90s = df0[dff['Decades'] == '2090-2099']
    tMod = 32
    tMod = 0
    pMod = 0.0393701
    pMod = 1
    if (variable == 'temp'):
        return {
            'data': [{
                'x': dfhist.Month,
                'y': dfhist.Temp - tMod,
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical'
            },{
                'x': df10s.Month,
                'y': df10s.Temp - tMod,
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#fecc5c'
                },
                'name': '2010-2019',
                'error_y': {
                    'type': 'data',
                    'array': df10s.TError,
                    'visible': variability
                }
            },{
                'x': df40s.Month,
                'y': df40s.Temp - tMod,
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#fd8d3c'
                },
                'name': '2040-2049',
                'error_y': {
                    'type': 'data',
                    'array': df40s.TError,
                    'visible': variability
                }
            },{
                'x': df60s.Month,
                'y': df60s.Temp - tMod,
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#f03b20'
                },
                'name': '2060-2069',
                'error_y': {
                    'type': 'data',
                    'array': df60s.TError,
                    'visible': variability
                }
            },{
                'x': df90s.Month,
                'y': df90s.Temp - tMod,
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#bd0026'
                },
                'name': '2090-2099',
                'error_y': {
                    'type': 'data',
                    'array': df90s.TError,
                    'visible': variability
                }
            }],
            'layout': {
                'barmode': 'grouped',
                'yaxis': {
                    'zeroline': 'false',
                    'zerolinecolor': '#efefef',
                    'zerolinewidth': 0.5
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
                    'y0': tMod, 'y1': tMod, 'yref': 'y',
                    'line': { 'width': 1 }
                }]
            }
        }
    else:
        return {
            'data': [{
                'x': dfhist.Month,
                'y': dfhist.Precip * pMod,
                'type': 'bar',
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical'
            },{
                'x': df10s.Month,
                'y': df10s.Precip * pMod,
                'type': 'bar',
                'marker': {
                    'color': '#bae4bc'
                },
                'name': '2010-2019',
                'error_y': {
                    'type': 'data',
                    'array': df10s.PError,
                    'visible': variability
                }
            },{
                'x': df40s.Month,
                'y': df40s.Precip * pMod,
                'type': 'bar',
                'marker': {
                    'color': '#7bccc4'
                },
                'name': '2040-2049',
                'error_y': {
                    'type': 'data',
                    'array': df40s.PError,
                    'visible': variability
                }
            },{
                'x': df60s.Month,
                'y': df60s.Precip * pMod,
                'type': 'bar',
                'marker': {
                    'color': '#43a2ca'
                },
                'name': '2060-2069',
                'error_y': {
                    'type': 'data',
                    'array': df60s.PError,
                    'visible': variability
                }
            },{
                'x': df90s.Month,
                'y': df90s.Precip * pMod,
                'type': 'bar',
                'marker': {
                    'color': '#0868ac'
                },
                'name': '2090-2099',
                'error_y': {
                    'type': 'data',
                    'array': df90s.PError,
                    'visible': variability
                }
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
