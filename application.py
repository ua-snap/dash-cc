"""
SNAP Community Charts / Community Climate Outlooks
"""

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import urllib
from flask import send_file
import flask
import io

import pandas as pd
import time
import os

df = None
co = pd.read_json('CommunityNames.json')
names = list(co.community)
units = 'imperial'
variability = True

app = dash.Dash(__name__)
# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server

Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
mean_cols = []

header_layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='columns',
            children=[
                html.Div(
                    className='column',
                    children=[
                        html.A(
                            href='https://snap.uaf.edu',
                            children=[
                                html.Img(src='assets/SNAP_acronym_color.svg')
                            ]
                        ),
                        html.Hr(),
                        html.H1(
                            'Community Charts',
                            className='title is-3'
                        ),
                        html.H2(
                            """
Explore temperature and precipitation projections for communities across Alaska and Canada shown here.
    """,
                            className='subtitle is-5'
                        ),
                        html.Div(
                            className='buttons',
                            children=[
                                html.A(
                                    'Download all Community Charts data',
                                    className='button is-info'
                                ),
                                html.A(
                                    'Go to SNAP home page',
                                    className='button is-link'
                                )
                            ]
                        )
                    ]
                ),
                html.Div(
                    className='column',
                    children=[
                        html.Img(src='assets/akcanada.svg')
                    ]
                )
            ]

        )
    ]
)

community_selector = html.Div(
    className='field',
    children=[
        html.Label('Type the name of a community in the box below to get started.', className='label'),
        html.Div(
            className='control',
            children=[
                dcc.Dropdown(
                    id='community',
                    options=[{'label':name, 'value':name} for name in names]
                )
            ]
        )
    ]
)

dataset_radio = html.Div(
    className='field',
    children=[
        html.Label('Dataset', className='label'),
        html.Div(
            className='control',
            children=[
                dcc.RadioItems(
                    labelClassName='radio',
                    options=[
                        {'label': ' Temperature', 'value': 'temp'},
                        {'label': ' Precipitation', 'value': 'precip'}
                    ],
                    id='variable',
                    value='temp'
                )
            ]
        )
    ]
)

units_radio = html.Div(
    className='field',
    children=[
        html.Label('Units', className='label'),
        html.Div(
            className='control',
            children=[
                dcc.RadioItems(
                    labelClassName='radio',
                    options=[
                        {'label': ' Imperial', 'value': 'imperial'},
                        {'label': ' Metric', 'value': 'metric'}
                    ],
                    id='units',
                    value='imperial'
                )
            ]
        )
    ]
)

baseline_radio = html.Div(
    className='field',
    children=[
        html.Label('Historical Baseline', className='label'),
        html.Div(
            className='control',
            children=[
                dcc.RadioItems(
                    labelClassName='radio',
                    options=[
                        {'label': ' CRU', 'value': 'cru32'},
                        {'label': ' PRISM', 'value': 'prism'}
                    ],
                    id='baseline',
                    value='cru32'
                )
            ]
        ),
        html.P("""
* Northwest Territories communities only available for CRU 3.2 baseline choice. 
""",
            className='help'
        )
    ]
)

rcp_radio = html.Div(
    className='field',
    children=[
        html.Label('Representative Concentration Pathways', className='label'),
        html.Div(
            className='control',
            children=[
                dcc.RadioItems(
                    labelClassName='radio',
                    options=[
                        {'label': ' Low (RCP4.5)', 'value': 'rcp45'},
                        {'label': ' Medium (RCP6.0)', 'value': 'rcp60'},
                        {'label': ' High (RCP8.5)', 'value': 'rcp85'}
                    ],
                    id='scenario',
                    value='rcp60'
                )
            ]
        )
    ]
)

variability_radio = html.Div(
    className='field',
    children=[
        html.Label('Inter-model Variability', className='label'),
        html.Div(
            className='control',
            children=[
                dcc.RadioItems(
                    labelClassName='radio',
                    options=[
                        {'label': ' Off', 'value': 'off'},
                        {'label': ' On', 'value': 'on'}
                    ],
                    id='variability',
                    value='off'
                )
            ]
        )
    ]
)
download_single_csv = html.Div(
    className='download',
    children=[
        html.Div(
            className='control',
            children=[
                html.A(
                    'Download Single Community (CSV)',
                    className='button is-success',
                    id='download_single',
                    href=''
                )
            ]
        )
    ]
)
download_all_csv = html.Div(
    className='download',
    children=[
        html.Div(
            className='control',
            children=[
                html.A(
                    'Dowload All Community Data (CSV)',
                    className='button is-success',
                    id='download_all',
                    href='http://data.snap.uaf.edu/data/Base/Other/Community_charts_tool_database/SNAP_comm_charts_export_20160926_fix_021119.csv'
                )
            ]
        )
    ]
)


form_layout = html.Div(
    className='container',
    children=[
        community_selector,
        html.Div(
            className='columns',
            children=[
                html.Div(
                    className='column',
                    children=[
                        dataset_radio,
                        units_radio,
                        baseline_radio
                    ]
                ),
                html.Div(
                    className='column',
                    children=[
                        rcp_radio,
                        variability_radio,
                        html.Div(
                            className='columns is-1',
                            children=[
                                html.Div(
                                    className='column is-half',
                                    children=[
                                        download_single_csv
                                    ]
                                ),
                                html.Div(
                                    className='column is-half',
                                    children=[
                                        download_all_csv
                                    ]
                                )

                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

graph_layout = html.Div(
    className='container',
    children=[
        dcc.Graph(id='ccharts')
    ]
)

explanations = html.Div(
    className='container',
    children=[
        dcc.Markdown("""
Due to variability among climate models and among years in a natural climate system, these graphs are useful for examining trends over time, rather than for precisely predicting monthly or yearly values.

### How to interpret climate outlooks for your community

You can examine SNAP community outlooks for certain key changes and threshold values—for example, higher mean monthly temperatures in the spring and fall may be of particular interest. This could signify any or all of these conditions:

* a longer growing season
* a loss of ice and/or frozen ground needed for travel or food storage
* a shift in precipitation from snow to rain, which impacts water storage capacity and surface water availability

Note: Precipitation may occur as either rain or snow, but is reported for all months in terms of rainwater equivalent.

Warmer, drier spring weather may also be an indicator for increased fire risk. In many locations, winter temperatures are projected to increase dramatically. Warmer winters may favor growth of species that are less cold-hardy (including desirable crops and invasive species), or it may decrease snowpack and increase the frequency of rain-on-snow events that impact wildlife. Higher temperatures across all seasons will likely impact permafrost and land-fast ice.
""",
            className='is-size-5 content'
        ),
        html.A(
            'Learn more about how we derived the community climate outlooks',
            id='button-show-about-derivation-modal',
            className='button is-info'
        )
    ]
)

footer = html.Footer('Footer content goes here', className='footer')

about_derivation_modal = html.Div(
    id='about-derivation-modal',
    className='modal',
    children=[
        html.Div(className='modal-background'),
        html.Div(className='modal-card', children=[
            html.Header(className='modal-card-head', children=[
                html.P(
                    'Community climate outlooks: core statistics and methods',
                    className='modal-card-title'
                ),
                html.Button(className='delete')
            ]),
            html.Section(className='modal-card-body', children=[
                dcc.Markdown(
"""
**Data sources**: Historical PRISM and CRU TS 3.2 climatology data (1961-1990) and downscaled outputs averaged from five GCMs.  [Learn more about how we downscale climate data from global to regional scales](https://www.snap.uaf.edu/methods/downscaling).

**We averaged results to smooth out short-term variability**. Results are averaged across decades to lessen the influence of normal year-to-year climate variability on projected values. Averaging also tends to make overall projection trends clearer. Uncertainty is associated with each of these graphed values, and stems from:

* modeling of atmospheric and oceanic movements used to create GCMs
* the downscaling process
* the assumptions made regarding greenhouse gas levels for each emissions scenario
* [Learn more about uncertainty in SNAP's climate research work](https://www.snap.uaf.edu/methods/uncertainty).

**Generally, precipitation is more uncertain than temperature**. And, although our models project increases in precipitation, water availability may decrease in some areas due to longer growing seasons and warmer weather.

""",
                    className='content'
                )
            ]),
            html.Footer(
                className='modal-card-foot',
                children=[
                    html.Button('Close', className='button is-primary')
                ]
            )
        ])
    ]
)

def section(content):
    """ Convenince function: Wrap content in a section div """
    return html.Div(className='section', children=[content])

app.layout = html.Div([
    section(header_layout),
    section(form_layout),
    section(graph_layout),
    section(explanations),
    footer,
    about_derivation_modal
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

    # Default!
    if community is None:
        community = 'Fairbanks'

    variability = variability == 'on'  # convert to boolean for use in configuring graph
    comm_file = './data/' + community + '_SNAP_comm_charts_export.csv'
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
@app.callback(
    dash.dependencies.Output('download_single', 'href'),
    [dash.dependencies.Input('community', 'value')])

def update_download_link(comm):
    return '/dash/urlToDownload?value={}'.format(comm)

@app.server.route('/dash/urlToDownload') 
def download_csv():
    value = flask.request.args.get('value')
    return send_file('./data/' + value + '_SNAP_comm_charts_export.csv',
                     mimetype='text/csv',
                     attachment_filename=value + '_charts.csv',
                     as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', False)
    app.run_server(debug=debug, port=port)
