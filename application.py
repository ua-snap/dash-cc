"""
SNAP Community Charts / Community Climate
"""
# pylint: disable=invalid-name, import-error, line-too-long, too-many-arguments

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.io as pio
import html as h
from flask import redirect,send_file
import flask
import re

import pandas as pd
import time
import os
from gui import layout

path_prefix = os.environ['REQUESTS_PATHNAME_PREFIX']

app = dash.Dash(__name__)
app.title = 'SNAP Community Climate Charts'
# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server

Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
mean_cols = []

# The next config sets a relative base path so we can deploy
# with custom URLs.
# https://community.plot.ly/t/dash-error-loading-layout/8139/6
app.config.requests_pathname_prefix = os.environ['REQUESTS_PATHNAME_PREFIX']

# Customize this layout to include Google Analytics
gtag_id = os.environ['GTAG_ID']
app.index_string = f'''
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-3978613-12"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{gtag_id}');
        </script>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
'''

app.layout = layout

@app.callback(
    Output('ccharts', 'figure'),
    inputs=[
        Input('community', 'value'),
        Input('decades', 'value'),
        Input('variable', 'value'),
        Input('scenario', 'value'),
        Input('variability', 'value'),
        Input('units', 'value'),
        Input('baseline', 'value')
    ]
)
def update_graph(community_raw, decades, variable, scenario, variability, units, baseline):
    """ Update the graph from user input """

    # Default!
    if community_raw is None:
        community_raw = 'Fairbanks'

    variability = variability == 'on'  # convert to boolean for use in configuring graph
    community = re.sub('[^A-Za-z0-9]+', '', community_raw)
    comm_file = 'https://s3-us-west-2.amazonaws.com/community-charts/data/' + community + '_SNAP_comm_charts_export.csv'
    df = pd.read_csv(comm_file)

    # [ML] maybe hardwire these? Not a huge time sink, but it could be made cleaner
    mean_cols = [col for col in df.columns if 'Mean' in col]
    sd_cols = [col for col in df.columns if 'Sd' in col]
    min_cols = [col for col in df.columns if 'Min' in col]
    max_cols = [col for col in df.columns if 'Max' in col]

    resolution_lu = {'cru32': '10min', 'prism': '2km' }
    variable_lu = {'temp':'Temperature', 'precip':'Precipitation'}
    # subset to the data we want to display using the callback variables
    dff = df[(df['community'] == community) & (df['resolution'] == resolution_lu[baseline]) & \
            (df['type'] == variable_lu[variable]) & (df['scenario'] == scenario) ]
    cols = mean_cols+sd_cols+['daterange','region'] # fun with list appending!
    dff = dff[cols] # grab just the cols we need
    baseline_df = df[(df['community'] == community) & (df['resolution'] == resolution_lu[baseline]) &\
                     (df['type'] == variable_lu[variable]) & (df['scenario'] == baseline.lower()) ]
    baseline_df = baseline_df[mean_cols] # grab just the cols we need

    # handle units conversion if needed:
    imperial_conversion_lu = {'temp':1.8,'precip':0.0393701}
    if units == 'imperial':
        # make things F/inches
        dff[mean_cols+sd_cols] = dff[mean_cols+sd_cols] * imperial_conversion_lu[variable]
        baseline_df[mean_cols] = baseline_df[mean_cols]* imperial_conversion_lu[variable]

    # scenario lookup
    scenario_lu = {'rcp45':'Low Emissions (RCP 4.5)',
                'rcp60':'Mid Emissions (RCP 6.0)',
                'rcp85':'High Emissions (RCP 8.5)'}
    emission_label = scenario_lu[scenario]

    # unit lookup
    unit_lu = {
        'temp': {
            'imperial': '&deg;F',
            'metric': '&deg;C'
        },
        'precip': {
            'imperial': 'in',
            'metric': 'mm'
        }
    }

    # baseline lookup
    baseline_lu = {'cru32':'CRU 3.2','prism':'PRISM'}
    baseline_label = baseline_lu[baseline]

    region_label = dff['region'].iloc[0]

    # set the freezing line for TEMPERATURE based on imperial or metric
    tMod = 0

    # Base Layout Item (for both variables)
    layout = {
            'barmode': 'grouped',
            'titlefont': {
                'family': 'Open Sans'
            },
            'annotations': [
            {
                'x': 0.5,
                'y': -0.20,
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'text': 'These plots are useful for examining possible trends over time, rather than for precisely predicting values.'
            },
            {
                'x': 0.5,
                'y': -0.26,
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'text': 'Credit: Scenarios Network for Alaska + Arctic Planning, University of Alaska Fairbanks.'
            }],
            'margin': {
                'l': 80,
                'r': 80,
                'b': 130,
                't': 100
            }
        }

    if variable == 'temp':
        if units == 'imperial':
            tMod = 32
        # Lookup table for included decades (default: 2010,2040,2060,2090)
        df_lu_full = {'2010-2019': {'color': '#ffd700'}, '2020-2029': {'color': '#ffc400'}, '2030-2039': {'color': '#ffb100'}, '2040-2049': {'color': '#ff9900'}, '2050-2059': {'color': '#ff7400'}, '2060-2069': {'color': '#ff5000'}, '2070-2079': {'color': '#e23300'}, '2080-2089': {'color': '#b61900'}, '2090-2099': {'color': '#8b0000'}}
        df_lu = dict()
        for decade in decades:
            df_lu[decade] = df_lu_full[decade]
        
        figure = {
            'data': [{
                'x': Months,
                'y': baseline_df[mean_cols].iloc[0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical '
            }]
        }
        for key in sorted(df_lu):
            df_l = dff[dff['daterange'] == key]
            figure['data'].append({
                'x': Months,
                'y': df_l[mean_cols].iloc[0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': df_lu[key]['color']
                },
                'name': key,
                'error_y': {
                    'type': 'data',
                    'array': df_l[sd_cols].iloc[0],
                    'visible': variability
                }
            })
        figure['layout'] = layout
        figure['layout']['title'] = '<b>Average Monthly Temperature for ' + community_raw + ', ' + region_label + '</b><br>Historical ' + baseline_label + ' and 5-Model Projected Average at ' + resolution_lu[baseline] + ' resolution, ' + emission_label + ' Scenario &nbsp;'
        figure['layout']['yaxis'] = {
            'zeroline': 'false',
            'zerolinecolor': '#efefef',
            'zerolinewidth': 0.5,
            'title': 'Temperature (' + unit_lu['temp'][units] + ')'
        }
        figure['layout']['shapes'] = [{
            'type': 'line',
            'x0': 0, 'x1': 1, 'xref': 'paper',
            'y0': tMod, 'y1': tMod, 'yref': 'y',
            'line': { 'width': 1 }
        }]
        return figure
    else:
        # Lookup table for included decades (default: 2010,2040,2060,2090)
        df_lu_full = {'2010-2019': {'color': '#7fffdf'}, '2020-2029': {'color': '#71e8ca'}, '2030-2039': {'color': '#63d2c1'}, '2040-2049': {'color': '#55bcb8'}, '2050-2059': {'color': '#47a6af'}, '2060-2069': {'color': '#3990a6'}, '2070-2079': {'color': '#2b7a9d'}, '2080-2089': {'color': '#1d6494'}, '2090-2099': {'color': '#104e8b'}}
        df_lu = dict()
        for decade in decades:
            df_lu[decade] = df_lu_full[decade]

        figure = {
            'data': [{
                'x': Months,
                'y': baseline_df[mean_cols].iloc[0],
                'type': 'bar',
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical '
            }]
        }
        for key in sorted(df_lu):
            df_l = dff[dff['daterange'] == key]
            figure['data'].append({
                'x': Months,
                'y': df_l[mean_cols].iloc[0],
                'type': 'bar',
                'marker': {
                    'color': df_lu[key]['color']
                },
                'name': key,
                'error_y': {
                    'type': 'data',
                    'array': df_l[sd_cols].iloc[0],
                    'visible': variability
                }
            })

        figure['layout'] = layout
        figure['layout']['title'] = '<b>Average Monthly Precipitation for ' + community_raw + ', ' + region_label + '</b><br>Historical ' + baseline_label + ' and 5-Model Projected Average at ' + resolution_lu[baseline] + ' resolution, ' + emission_label + ' Scenario &nbsp;'
        figure['layout']['yaxis'] = {
            'title': 'Precipitation (' + unit_lu['precip'][units] +')'
        }
        return figure
@app.callback(
    Output('download_single', 'href'),
    [Input('community', 'value')])

def update_download_link(comm):
    return path_prefix + 'dash/dlCSV?value={}'.format(comm)

@app.server.route('/dash/dlCSV') 
def download_csv():
    value = flask.request.args.get('value')
    value = h.unescape(value)
    value = re.sub('[^A-Za-z0-9]+', '', value)
    return redirect('https://s3-us-west-2.amazonaws.com/community-charts/data/' + value + '_SNAP_comm_charts_export.csv')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', False)
    app.run_server(debug=debug, port=port)
