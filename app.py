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

df = []
co = pd.read_json('CommunityNames.json')
names = list(co.community)
units = 'imperial'
variability = True

app = dash.Dash(__name__)
Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
mean_cols = []

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Community Charts'),
    dcc.Dropdown(
        id='community',
        options=[{'label':name, 'value':name} for name in names]
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
            {'label': 'CRU', 'value': 'cru32'},
            {'label': 'PRISM', 'value': 'prism'}
        ],
        id='baseline',
        value='cru32'
    ),
    html.Label('Intermodel Variability'),
    dcc.RadioItems(
        options=[
            {'label': 'Off', 'value': 'off'},
            {'label': 'On', 'value': 'on'}
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
        Input('variability', 'value'),
        Input('units', 'value'),
        Input('baseline', 'value')
    ]
)
def update_graph(community, variable, scenario, variability, units, baseline):
    """ Update the graph from user input """

    variability = variability == 'on'  # convert to boolean for use in configuring graph
    comm_file = './communities_csvs/' + community + '_SNAP_comm_charts_export.csv'
    df = pd.read_csv(comm_file)
    dff = df[df['community'] == community]
    df2 = dff[dff['resolution'] == '2km']
    if (variable == 'temp'):
        df0 = df2[df2['type'] == 'Temperature']
    else:
        df0 = df2[df2['type'] == 'Precipitation']

    df1 = df0[df0['scenario'] == scenario]
    df3 = df0[df0['scenario'] == baseline]

    mean_cols = [col for col in df.columns if 'Mean' in col]
    sd_cols = [col for col in df.columns if 'Sd' in col]
    min_cols = [col for col in df.columns if 'Min' in col]
    max_cols = [col for col in df.columns if 'Max' in col]

    dfhist = df3[df3['daterange'] == 'Historical']
    df10s = df1[df1['daterange'] == '2010-2019']
    df40s = df1[df1['daterange'] == '2040-2049']
    df60s = df1[df1['daterange'] == '2060-2069']
    df90s = df1[df1['daterange'] == '2090-2099']

    tMod = 0
    pMod = 1
    units = 'standard'
    if (units  == 'imperial'):
        dfhist.Temp = dfhist.Temp.multiply(1.8) + 32
        df10s.Temp = df10s.Temp.multiply(1.8) + 32
        df40s.Temp = df40s.Temp.multiply(1.8) + 32
        df60s.Temp = df60s.Temp.multiply(1.8) + 32
        df90s.Temp = df90s.Temp.multiply(1.8) + 32
        dfhist.Precip = dfhist.Precip * 0.0393701
        df10s.Precip = df10s.Precip * 0.0393701
        df40s.Precip = df40s.Precip * 0.0393701
        df60s.Precip = df60s.Precip * 0.0393701
        df90s.Precip = df90s.Precip * 0.0393701
        tMod = 32
    if (variable == 'temp'):
        return {
            'data': [{
                'x': Months,
                'y': dfhist[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical'
            },{
                'x': Months,
                'y': df10s[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#fecc5c'
                },
                'name': '2010-2019',
                'error_y': {
                    'type': 'data',
                    'array': df10s[sd_cols].T.iloc[:,0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df40s[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#fd8d3c'
                },
                'name': '2040-2049',
                'error_y': {
                    'type': 'data',
                    'array': df40s[sd_cols].T.iloc[:,0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df60s[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#f03b20'
                },
                'name': '2060-2069',
                'error_y': {
                    'type': 'data',
                    'array': df60s[sd_cols].T.iloc[:,0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df90s[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#bd0026'
                },
                'name': '2090-2099',
                'error_y': {
                    'type': 'data',
                    'array': df90s[sd_cols].T.iloc[:,0],
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
                'x': Months,
                'y': dfhist[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical'
            },{
                'x': Months,
                'y': df10s[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'marker': {
                    'color': '#bae4bc'
                },
                'name': '2010-2019',
                'error_y': {
                    'type': 'data',
                    'array': df10s[sd_cols].T.iloc[:,0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df40s[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'marker': {
                    'color': '#7bccc4'
                },
                'name': '2040-2049',
                'error_y': {
                    'type': 'data',
                    'array': df40s[sd_cols].T.iloc[:,0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df60s[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'marker': {
                    'color': '#43a2ca'
                },
                'name': '2060-2069',
                'error_y': {
                    'type': 'data',
                    'array': df60s[sd_cols].T.iloc[:,0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df90s[mean_cols].T.iloc[:,0],
                'type': 'bar',
                'marker': {
                    'color': '#0868ac'
                },
                'name': '2090-2099',
                'error_y': {
                    'type': 'data',
                    'array': df90s[sd_cols].T.iloc[:,0],
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
