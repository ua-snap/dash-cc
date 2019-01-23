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
    html.Div(dcc.Markdown('xyz',id='div1')),
    html.Button('Temperature', id='temperature', n_clicks_timestamp=0),
    html.Button('Precipitation', id='precipitation', n_clicks_timestamp=0),
    html.Div(dcc.Markdown('Units',id='div1.5')),
    html.Button('Imperial', id='units_im', n_clicks_timestamp=0),
    html.Button('Metric', id='units_m', n_clicks_timestamp=0),
    html.Div(dcc.Markdown('abcd',id='div2')),
    html.Button('RCP45', id='rcp45', n_clicks_timestamp=0),
    html.Button('RCP60', id='rcp60', n_clicks_timestamp=0),
    html.Button('RCP85', id='rcp85', n_clicks_timestamp=0),
    html.Div(dcc.Markdown('Historical Baseline',id='div3')),
    html.Button('Off', id='base_cru', n_clicks_timestamp=0),
    html.Button('On', id='base_prism', n_clicks_timestamp=0),
    html.Div(dcc.Markdown('Intermodel Variability',id='div4')),
    html.Button('Off', id='vari_off', n_clicks_timestamp=0),
    html.Button('On', id='vari_on', n_clicks_timestamp=0),
    dcc.Graph(id='ccharts')
], className="container")

@app.callback(dash.dependencies.Output('div1', 'children'),
    inputs=[
      dash.dependencies.Input('temperature', 'n_clicks_timestamp'),
      dash.dependencies.Input('precipitation', 'n_clicks_timestamp')])
def update_div1(temp, precip):
    if (precip > temp):
        return "Precip CLICKED"
    else:
        return "Temp CLICKED"
@app.callback(dash.dependencies.Output('div2', 'children'),
    inputs=[
      dash.dependencies.Input('rcp45', 'n_clicks_timestamp'),
      dash.dependencies.Input('rcp60', 'n_clicks_timestamp'),
      dash.dependencies.Input('rcp85', 'n_clicks_timestamp')])
def update_div2(rcp45, rcp60, rcp85):
    if (rcp45 > rcp60 and rcp45 > rcp85):
        return "RCP45 CLICKED"
    elif (rcp60 > rcp45 and rcp60 > rcp85):
        return "RCP60 CLICKED"
    else:
        return "RCP85 CLICKED"
@app.callback(dash.dependencies.Output('div4', 'children'),
    inputs=[
      dash.dependencies.Input('vari_on', 'n_clicks_timestamp'),
      dash.dependencies.Input('vari_off', 'n_clicks_timestamp')])
def update_div4(von,voff):
    if (von > voff):
        variability = True
        return 'On'
    else:
        variability = False
        return 'Off'

@app.callback(dash.dependencies.Output('ccharts', 'figure'),
    inputs=[
      dash.dependencies.Input('community', 'value'), 
      dash.dependencies.Input('temperature', 'n_clicks_timestamp'), 
      dash.dependencies.Input('precipitation', 'n_clicks_timestamp'),
      dash.dependencies.Input('rcp45', 'n_clicks_timestamp'),
      dash.dependencies.Input('rcp60', 'n_clicks_timestamp'),
      dash.dependencies.Input('rcp85', 'n_clicks_timestamp'),
      dash.dependencies.Input('vari_on', 'n_clicks_timestamp'),
      dash.dependencies.Input('vari_off', 'n_clicks_timestamp')
    ])
def update_graph(selected_dropdown_value, temp, precip, rcp45, rcp60, rcp85, von, voff):
    if (von > voff):
        variability = True
    else:
        variability = False
    dff = df[df['Community'] == selected_dropdown_value]
    df0 = dff;
    if (rcp45 > rcp60 and rcp45 > rcp85):
        df0 = df[dff['Scenario'] == '4.5']
    elif (rcp60 > rcp45 and rcp60 > rcp85):
        df0 = df[dff['Scenario'] == '6.0']
    else:
        df0 = df[dff['Scenario'] == '8.5']
    dfhist = df[dff['Decades'] == '1961-1990']
    df10s = df0[dff['Decades'] == '2010-2019']
    df40s = df0[dff['Decades'] == '2090-2099']
    df60s = df0[dff['Decades'] == '2060-2069']
    df90s = df0[dff['Decades'] == '2090-2099']
    if (temp > precip or temp == precip):
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
                    'array': df10s.TError,
                    'visible': variability
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
                    'array': df40s.TError,
                    'visible': variability
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
                    'array': df60s.TError,
                    'visible': variability
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
                    'y0': 32, 'y1': 32, 'yref': 'y',
                    'line': { 'width': 1 }
                }]
            }
        }
    elif(precip > temp):
        return {
            'data': [{
                'x': dfhist.Month,
                'y': dfhist.Precip,
                'type': 'bar',
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical'
            },{
                'x': df10s.Month,
                'y': df10s.Precip,
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
                'y': df40s.Precip,
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
                'y': df60s.Precip,
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
                'y': df90s.Precip,
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
