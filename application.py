"""
SNAP Community Charts / Community Climate Outlooks
"""

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.io as pio
import html as h
import urllib
from flask import send_file
import flask
import io
import re

import pandas as pd
import time
import os

df = None
co = pd.read_json('CommunityNames.json')
names = list(co.community)

app = dash.Dash(__name__)
app.title = 'SNAP Community Climate Outlook Charts'
# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server

Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
mean_cols = []

community_selector = html.Div(
    className='field',
    children=[
        html.Label('Type the name of a community in the box below to get started.', className='label'),
        html.Div(
            className='control',
            children=[
                dcc.Dropdown(
                    id='community',
                    options=[{'label':name, 'value':name} for name in names],
                    value='Fairbanks'
                )
            ]
        )
    ]
)

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
                            'Community Climate Outlook Charts',
                            className='title is-3'
                        ),
                        html.H2(
                            """
Explore temperature and precipitation projections for selected communities
across Alaska and central and northwestern Canada. Because natural climate
systems and models are variable, these graphs are best for studying trends,
rather than for precisely predicting monthly or yearly values.
    """,
                            className='subtitle is-5'
                        ),
                        community_selector
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
download_svg = html.Div(
    className='download',
    children=[
        html.Div(
            className='control',
            children=[
                html.A(
                    'Download SVG',
                    className='button is-info',
                    id='download_svg',
                    href=''
                )
            ]
        )
    ]
)
download_png = html.Div(
    className='download',
    children=[
        html.Div(
            className='control',
            children=[
                html.A(
                    'Download PNG',
                    className='button is-info',
                    id='download_png',
                    href=''
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
        #community_selector,
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
config = {
    'toImageButtonOptions': {
        'title': 'Export to SVG',
        'format': 'svg',
        'filename': 'custom_image',
        'height': 600,
        'width': 1600,
        'scale': 1
    },
    'modeBarButtonsToRemove': [
        'zoom2d',
        'sendToCloud',
        'pan2d',
        'select2d',
        'lasso2d',
        'toggleSpikeLines'
    ]
}

graph_layout = html.Div(
    className='container',
    children=[
        dcc.Graph(id='ccharts', config=config),
        #download_svg,
        #download_png
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

### Representative Concentration Pathways

The four different Representative Concentration Pathways (RCPs) adopted by the IPCC as of its fifth Assessment Report (AR5) in 2014 depict a range of possible future atmospheric greenhouse gas concentrations. These pathways represent four climate futures, extrapolated out to the year 2100, based on a range of possible future human behaviors. Their numerical values (2.6, 4.5, 6.0, and 8.5) measure radiative forcing values (W/m2) relative to pre-industrial values. For example, RPC 6.0 projects that in 2100 the concentration of greenhouse gases will be such that the solar energy absorbed by each square meter of Earth (rather than radiated back into space) will be, on average, six watts per meter squared greater than it was in 1750.

* RCP 4.5 (low)
This pathway assumes that emissions peak around 2040, and that radiative forcing is stabilized shortly after 2100. SNAP terms this the “low” scenario. It was developed at the Pacific Northwest National Laboratory’s Joint Global Change Research Institute in the United States.

* RCP 6.0 (medium)
This RCP assumes that a range of technologies and strategies for reducing greenhouse gas emissions are developed, allowing emissions to peak around 2080, then decline, with total radiative forcing stabilized shortly after 2100. This is SNAP’s “medium” scenario. It was developed at the National Institute for Environmental Studies in Japan.

* RCP 8.5 (high)
This potential future is characterized by increasing greenhouse gas emissions continuing through the 21st century. SNAP uses this as its “high” scenario. It was developed at the International Institute for Applied Systems Analysis, Austria.

Note: An additional set of projections, RCP 2.6, posits that greenhouse gas emissions peak between 2010 and 2020 and decline substantially thereafter. It was developed by at the PBL Netherlands Environmental Assessment Agency. Because its premises are unrealistic in light of current global emissions, SNAP does not use this pathway for modeling purposes.

### Historical Baseline

Climate Research Unit (CRU) and Parameter elevation Regression on Independent Slopes Model (PRISM) refer to two different models used by different research groups to create gridded climate datasets from available historical information.

Historical climate information is available from only a limited number of climate stations across Alaska and western Canada. These climate stations are not only few and far between, but also tend to be located in low-lying towns and cities, rather than in inaccessible locations such as mountain ranges. Thus, estimating historical (baseline) data for regularly spaced intervals on a map (gridded data) poses a challenge for modelers.

Most of SNAP's downscaled modeling relies on PRISM as a baseline, as described here: Downscaling Methods. PRISM creates fine-scale climate grids using not only climate station data but also the location of each grid point relative to nearby climate stations, and its elevation, slope, direction of slope, proximity to coastlines, and other features. Baseline historical PRISM data and future projections downscaled using two-kilometer PRISM baseline grids represent one of the choices available in this chart tool.

CRU grids rely on similar, but not identical, modeling techniques. Thus, comparing PRISM-downscaled data to CRU-downscaled data offers a perspective on model uncertainty related to the challenges of creating gridded climate data from limited historical data. CRU data are coarser, but cover a broader area, including Canada's Northwest Territories, for which PRISM data are not currently available. Baseline CRU data and future projections downscaled using CRU grids at 10' latitude and longitude (about 18 km) represent the other choice available in this chart tool.

### Variability Among Models

SNAP uses five different global circulation models (GCMs) as a basis for our down-scaled climate projections, as explained on this website under "Methods". Slight variations between these models allow us to consider a range of possible future climate conditions. This chart tool offers users a way to visualize this variability.

If you click on "Range", you will see a bar graph for your selected community with black lines extending above and below each bar. The colored bars represent the average (mean) values from all five models, and the black lines show the lowest and highest values among the five models used. Baseline years have no range values, because they are derived directly from climate station data, rather than from the five models.

If you click on "Off", the bar chart will show the five-model average with no black lines indicating range.

### Community Climate Outlooks: Core Statistics and Methods

Data sources: Historical PRISM and CRU TS 3.2 climatology data (1961-1990) and downscaled outputs averaged from five GCMs. Learn more about how we downscale climate data from global to regional scales.

We averaged results to smooth out short-term variability. Results are averaged across decades to lessen the influence of normal year-to-year climate variability on projected values. Averaging also tends to make overall projection trends clearer. Uncertainty is associated with each of these graphed values, and stems from:

* modeling of atmospheric and oceanic movements used to create GCMs
* the downscaling process
* the assumptions made regarding greenhouse gas levels for each emissions scenario

Learn more about uncertainty in SNAP’s climate research work.
Generally, precipitation is more uncertain than temperature. And, although our models project increases in precipitation, water availability may decrease in some areas due to longer growing seasons and warmer weather.
""",
            className='is-size-5 content'
        ),
        html.A(
            'Learn more about how we derived the community climate outlooks',
            id='button-show-about-derivation-modal',
            className='button is-info',
            href='https://www.snap.uaf.edu/methods/uncertainty'
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
    community = re.sub('[^A-Za-z0-9]+', '', community)
    comm_file = './data/' + community + '_SNAP_comm_charts_export.csv'
    df = pd.read_csv(comm_file)

    # [ML] maybe hardwire these? Not a huge time sink, but it could be made cleaner
    mean_cols = [col for col in df.columns if 'Mean' in col]
    sd_cols = [col for col in df.columns if 'Sd' in col]
    min_cols = [col for col in df.columns if 'Min' in col]
    max_cols = [col for col in df.columns if 'Max' in col]

    variable_lu = {'temp':'Temperature', 'precip':'Precipitation'}

    # subset to the data we want to display using the callback variables
    dff = df[(df['community'] == community) & (df['resolution'] == '2km') & \
            (df['type'] == variable_lu[variable]) & (df['scenario'] == scenario) ]
    cols = mean_cols+sd_cols+['daterange','region'] # fun with list appending! 
    dff = dff[cols] # grab just the cols we need
    baseline_df = df[(df['community'] == community) & (df['resolution'] == '2km') &\
                     (df['type'] == variable_lu[variable]) & (df['scenario'] == baseline.lower()) ]
    baseline_df = baseline_df[mean_cols] # grab just the cols we need

    # handle units conversion if needed:
    imperial_conversion_lu = {'temp':1.8,'precip':0.0393701}
    if units == 'imperial':
        # make things F/inches
        dff[mean_cols+sd_cols] = dff[mean_cols+sd_cols] * imperial_conversion_lu[variable]
        baseline_df[mean_cols] = baseline_df[mean_cols]* imperial_conversion_lu[variable]

    # scenario lookup
    scenario_lu = {'rcp45':'Low-Range Emissions (RCP 4.5)', 
                'rcp60':'Mid-Range Emissions (RCP 6.0)', 
                'rcp85':'High-Range Emissions (RCP 8.5)'}
    emission_label = scenario_lu[scenario]

    # baseline lookup
    baseline_lu = {'cru32':'CRU 3.2','prism':'Prism'}
    baseline_label = baseline_lu[baseline]

    region_label = dff['region'].iloc[0]

    # subset to some dataframes for plotting. This can be improved.
    df10s = dff[dff['daterange'] == '2010-2019']
    df40s = dff[dff['daterange'] == '2040-2049']
    df60s = dff[dff['daterange'] == '2060-2069']
    df90s = dff[dff['daterange'] == '2090-2099']

    # set the freezing line for TEMPERATURE based on imperial or metric
    tMod = 0
    if variable == 'temp':
        if units == 'imperial':
            tMod = 32

        figure = {
        #return {
            'data': [{
                'x': Months,
                'y': baseline_df[mean_cols].iloc[0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical'
            },{
                'x': Months,
                'y': df10s[mean_cols].iloc[0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#fecc5c'
                },
                'name': '2010-2019',
                'error_y': {
                    'type': 'data',
                    'array': df10s[sd_cols].iloc[0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df40s[mean_cols].iloc[0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#fd8d3c'
                },
                'name': '2040-2049',
                'error_y': {
                    'type': 'data',
                    'array': df40s[sd_cols].iloc[0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df60s[mean_cols].iloc[0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#f03b20'
                },
                'name': '2060-2069',
                'error_y': {
                    'type': 'data',
                    'array': df60s[sd_cols].iloc[0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df90s[mean_cols].iloc[0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#bd0026'
                },
                'name': '2090-2099',
                'error_y': {
                    'type': 'data',
                    'array': df90s[sd_cols].iloc[0],
                    'visible': variability
                }
            }],
            'layout': {
                'barmode': 'group',
                'title': '<b>Average Monthly Temperature for ' + community + ', ' + region_label + '</b><br>Historical ' + baseline_label + ' and 5-Model Projected Average at 2km resolution, ' + emission_label + ' Scenario &nbsp;',
                'titlefont': {
                    'size': 20,
                    'family': 'serif'
                },
                'annotations': [{
                    'x': 0.5004254919715793,
                    'y': -0.16191064079952971,
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'text': 'Due to variability among climate models and among years in a natural climate system, these graphs are useful for examining trends over time, rather than for precisely predicting monthly or yearly values.'
                }],
                'yaxis': {
                    'zeroline': 'false',
                    'zerolinecolor': '#efefef',
                    'zerolinewidth': 0.5,
                    'title': 'Temperature'
                },
                'margin': {
                    'l': 50,
                    'r': 50,
                    'b': 100,
                    't': 50
                },
                'shapes': [{
                    'type': 'line',
                    'x0': 0, 'x1': 1, 'xref': 'paper',
                    'y0': tMod, 'y1': tMod, 'yref': 'y',
                    'line': { 'width': 1 }
                }]

            }
        }

        
        figure['layout']['yaxis']['zeroline'] = False
        #img_bytes = pio.to_image(figure, format='svg')
        #pio.write_image(figure, 'images/fig1.png', width=1600, height=600, scale=2)
        figure['layout']['yaxis']['zeroline'] = 'false'
        figure['layout']['barmode'] = 'grouped'
        return figure
    else:
        figure = {
        #return {
            'data': [{
                'x': Months,
                'y': baseline_df[mean_cols].iloc[0],
                'type': 'bar',
                'marker': {
                    'color': '#999999'
                },
                'name': 'Historical'
            },{
                'x': Months,
                'y': df10s[mean_cols].iloc[0],
                'type': 'bar',
                'marker': {
                    'color': '#bae4bc'
                },
                'name': '2010-2019',
                'error_y': {
                    'type': 'data',
                    'array': df10s[sd_cols].iloc[0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df40s[mean_cols].iloc[0],
                'type': 'bar',
                'marker': {
                    'color': '#7bccc4'
                },
                'name': '2040-2049',
                'error_y': {
                    'type': 'data',
                    'array': df40s[sd_cols].iloc[0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df60s[mean_cols].iloc[0],
                'type': 'bar',
                'marker': {
                    'color': '#43a2ca'
                },
                'name': '2060-2069',
                'error_y': {
                    'type': 'data',
                    'array': df60s[sd_cols].iloc[0],
                    'visible': variability
                }
            },{
                'x': Months,
                'y': df90s[mean_cols].iloc[0],
                'type': 'bar',
                'marker': {
                    'color': '#0868ac'
                },
                'name': '2090-2099',
                'error_y': {
                    'type': 'data',
                    'array': df90s[sd_cols].iloc[0],
                    'visible': variability
                }
            }],
            'layout': {
                'barmode': 'group',
                'title': '<b>Average Monthly Precipitation for ' + community + ', ' + region_label + '</b><br>Historical ' + baseline_label + ' and 5-Model Projected Average at 2km resolution, ' + emission_label + ' Scenario &nbsp;',
                'titlefont': {
                    'size': 20,
                    'family': 'serif'
                },
                'annotations': [{
                    'x': 0.5004254919715793,
                    'y': -0.16191064079952971,
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'text': 'Due to variability among climate models and among years in a natural climate system, these graphs are useful for examining trends over time, rather than for precisely predicting monthly or yearly values.'
                }],
                'yaxis': {
                    'title': 'Precipitation'
                },
                'margin': {
                    'l': 50,
                    'r': 50,
                    'b': 100,
                    't': 50
                }
            }
        }
        return figure
@app.callback(
    Output('download_single', 'href'),
    [Input('community', 'value')])

def update_download_link(comm):
    return '/dash/dlCSV?value={}'.format(comm)

@app.server.route('/dash/dlCSV') 
def download_csv():
    value = flask.request.args.get('value')
    value = h.unescape(value)
    value = re.sub('[^A-Za-z0-9]+', '', value)
    return send_file('./data/' + value + '_SNAP_comm_charts_export.csv',
                     mimetype='text/csv',
                     attachment_filename=value + '_charts.csv',
                     as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    debug = os.environ.get('DEBUG', False)
    app.run_server(debug=debug, port=port)
