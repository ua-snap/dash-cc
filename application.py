"""
SNAP Community Charts / Community Climate
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
app.title = 'SNAP Community Climate Charts'
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
  #  className='container',
  #  children=[
        html.Div(
            className='columns',
            children=[
                html.Div(
                    className='column is-three-fifths',
                    children=[
                        community_selector
                    ]

                )
            ]

        )
  #  ]
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
        html.Label('Scenarios (RCPs)', className='label'),
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
                    className='button is-info',
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
                    'Download All Data and View Metadata',
                    className='button is-info',
                    id='download_all',
                    #href='http://data.snap.uaf.edu/data/Base/Other/Community_charts_tool_database/SNAP_comm_charts_export_20160926_fix_021119.csv'
                    href='http://ckan.snap.uaf.edu/dataset/community-charts-temperature-and-precipitation'
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
        'title': 'Export to PNG',
        'format': 'png',
        'filename': 'CommunityChart',
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
### Learn more about the variables used in this tool

Due to variability among climate models and among years in a natural climate system, these graphs are useful for examining trends over time, rather than for precisely predicting monthly or yearly values.

#### How to interpret climate outlooks for your community

You can examine SNAP community outlooks for certain key changes and threshold values—for example, higher mean monthly temperatures in the spring and fall may be of particular interest. This could signify any or all of these conditions:

* a longer growing season
* a loss of ice and/or frozen ground needed for travel or food storage
* a shift in precipitation from snow to rain, which impacts water storage capacity and surface water availability

Note: Precipitation may occur as either rain or snow, but is reported for all months in terms of rainwater equivalent.

Warmer, drier spring weather may also be an indicator for increased fire risk. In many locations, winter temperatures are projected to increase dramatically. Warmer winters may favor growth of species that are less cold-hardy (including desirable crops and invasive species), or it may decrease snowpack and increase the frequency of rain-on-snow events that impact wildlife. Higher temperatures across all seasons will likely impact permafrost and land-fast ice.

#### Representative Concentration Pathways

RCPs describe paths to future climates based on atmospheric greenhouse gas concentrations. They represent climate futures—scenarios—extrapolated out to the year 2100, based on a range of possible future human behaviors. RCPs provide a basis for comparison and a “common language” for modelers to share their work.

The RCP values 4.5, 6.0, and 8.5 indicate projected radiative forcing values—the difference between solar energy absorbed by Earth vs. energy radiated back to space—measured in watts per square meter. RCP X projects that in 2100 the concentration of greenhouse gases will be such that each square meter of Earth will absorb X times more solar energy than it did in 1750.

* RCP 4.5 — “low” scenario. Assumes that new technologies and socioeconomic strategies cause emissions to peak in 2040 and radiative forcing to stabilize after 2100. 
* RCP 6.0 — “medium” scenario. Assumes that emissions peak in 2080 and radiative forcing stabilizes after 2100.
* RCP 8.5 — “high” scenario. Emissions increase through the 21st century.

#### Historical Baseline

Making climate projections requires use of historical data as a starting point, or baseline. It’s challenging to estimate historical data across a map grid because these data are only available from a few climate stations across Alaska and western Canada. Also, stations are often clustered in low-lying communities rather than across remote locations such as mountain ranges. Ideally, estimates should be made at regular intervals, or on a grid.  

To get around this, two types of models are used to create gridded climate datasets from available historical values: Parameter elevation Regression on Independent Slopes Model (PRISM) and Climate Research Unit (CRU).

PRISM and CRU can each be used to create climate grids using climate station data, grid point locations relative to nearby stations, elevation, slope, aspect, proximity to coastlines, and other features. CRU data are coarser but cover a broader area than PRISM. 

For comparison and a look at model uncertainty related to the challenges of creating gridded climate data from limited historical data, this tool offers both:
* Baseline PRISM data and future projections downscaled using 2km PRISM grids
* Baseline CRU data and future projections downscaled using ~18km CRU grids

###### More details
* [SNAP data sources](https://www.snap.uaf.edu/methods/data-sources)
* [SNAP’s downscaling process](https://www.snap.uaf.edu/methods/downscaling)

#### Variability Among Models

A Global Climate Model (GCM) is a type of General Circulation Model that focuses on projections of climate change by simulating how Earth’s physical processes respond to increasing greenhouse gas concentrations. Slight variations between these models allow us to consider a range of possible future climate conditions. SNAP projections use 5 GCMs that perform best in the Arctic, as well as an average of the 5 selected models. 

This tool offers users a way to hide and show this variability: 
* Click "Range" to see a bar graph for your selected community. Notice the black lines extending above and below each bar. The bars represent the average (mean) values from all 5 models, and the black lines show the lowest and highest values among the 5 models used. Baseline years have no range values because they are derived directly from climate station data, rather than from the 5 models.
* Click "Off" to hide range values and show only the 5-model average.

###### More details
* [SNAP’s model evaluation and selection process](https://www.snap.uaf.edu/methods/model-selection)
* [General Circulation Models and Global Climate Models](https://www.sciencedaily.com/terms/global_climate_model.htm)

""",
            className='is-size-5 content'
        )
    ]
)

footer = html.Footer(
    className='footer has-text-centered',
    children=[
        html.Div(
            children=[
                html.A(
                    href='https://snap.uaf.edu',
                    target='_blank',
                    className='level-item',
                    children=[
                        html.Img(
                            src='assets/SNAP.svg'
                        )
                    ]
                ),
                html.A(
                    href='https://uaf.edu/uaf/',
                    target='_blank',
                    className='level-item',
                    children=[
                        html.Img(
                            src='assets/UAF.svg'
                        )
                    ]
                ),
                html.A(
                    href='https://www.gov.nt.ca/',
                    target='_blank',
                    className='level-item',
                    children=[
                        html.Img(
                            src='assets/NWT.svg'
                        )
                    ]
                )
            ]
        ),
        dcc.Markdown(
            """
This tool is part of an ongoing collaboration between SNAP and the Government of Northwest Territories. We are working to make a wide range of downscaled climate products that are easily accessible, flexibly usable, and fully interpreted and understandable to users in the Northwest Territories, while making these products relevant at a broad geographic scale.

UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual. [Statement of Nondiscrimination](https://www.alaska.edu/nondiscrimination/)
            """,
            className='content is-size-6'
        )
    ]
)


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
#### Learn more about the variables used in this tool

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

header_section = html.Div(
    className='header',
    children=[
        html.Div(
            className='container',
            children=[
                html.Div(
                    className='section',
                    children=[
                        html.Div(
                            className='header--logo',
                            children=[
                                html.A(
                                    className='header--snap-link',
                                    children=[
                                        html.Img(src='assets/SNAP.svg')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='header--map',
                            children=[
                                html.Div(
                                    children=[
                                        html.Img(src='assets/akcanada.svg')
                                    ]
                                )
                            ]
                        ),
                        html.Div(
                            className='header--titles',
                            children=[
                                html.H1(
                                    'Community Climate Charts',
                                    className='title is-2'
                                ),
                                html.H2(
                                    'Explore temperature and precipitation projections for selected communities across Alaska and central and northwestern Canada.',
                                    className='subtitle is-4'
                                )
                            ]

                        )
                    ]
                )
            ]
        )
    ]
)

main_layout = html.Div(
    className='container',
            children=[
                header_layout,
                form_layout,
                graph_layout,
                explanations
            ]
)

app.layout = html.Div(
    children=[
        header_section,
        main_layout,
        footer
    ]
)



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

    unit_conversion_lu = {
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
                'name': 'Historical '
            },{
                'x': Months,
                'y': df10s[mean_cols].iloc[0],
                'type': 'bar',
                'base': tMod,
                'marker': {
                    'color': '#fecc5c'
                },
                'name': '2010-2019 ',
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
                'name': '2040-2049 ',
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
                'name': '2060-2069 ',
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
                'name': '2090-2099 ',
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
                'yaxis': {
                    'zeroline': 'false',
                    'zerolinecolor': '#efefef',
                    'zerolinewidth': 0.5,
                    'title': 'Temperature (' + unit_conversion_lu['temp'][units] + ')'
                },
                'margin': {
                    'l': 50,
                    'r': 50,
                    'b': 130,
                    't': 100
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
                'name': 'Historical '
            },{
                'x': Months,
                'y': df10s[mean_cols].iloc[0],
                'type': 'bar',
                'marker': {
                    'color': '#bae4bc'
                },
                'name': '2010-2019 ',
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
                'name': '2040-2049 ',
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
                'name': '2060-2069 ',
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
                'name': '2090-2099 ',
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
                'yaxis': {
                    'title': 'Precipitation (' + unit_conversion_lu['precip'][units] +')'
                },
                'margin': {
                    'l': 50,
                    'r': 50,
                    'b': 130,
                    't': 100
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
