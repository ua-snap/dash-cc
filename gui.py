"""
SNAP Community Charts / Community Climate
"""

import os
import json
import plotly.graph_objs as go
from dash import dcc
from dash import html
import pandas as pd

df = None
co = pd.read_json('CommunityNames.json')
names = list(co.community)
path_prefix = os.environ['DASH_REQUESTS_PATHNAME_PREFIX']

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
                    value='Fairbanks, Alaska'
                )
            ]
        )
    ]
)

decade_selector = html.Div(
    className='field',
    children=[
        html.Label('Select the decades of interest', className='label'),
        html.Div(
            className='control',
            children=[
                dcc.Dropdown(
                    id='decades',
                    options=[
                        {'label': '2010-2019', 'value': '2010-2019'},
                        {'label': '2020-2029', 'value': '2020-2029'},
                        {'label': '2030-2039', 'value': '2030-2039'},
                        {'label': '2040-2049', 'value': '2040-2049'},
                        {'label': '2050-2059', 'value': '2050-2059'},
                        {'label': '2060-2069', 'value': '2060-2069'},
                        {'label': '2070-2079', 'value': '2070-2079'},
                        {'label': '2080-2089', 'value': '2080-2089'},
                        {'label': '2090-2099', 'value': '2090-2099'},
                    ],
                    value=['2010-2019','2040-2049','2060-2069','2090-2099'],
                    multi=True
                )
            ]
        )
    ]
)

header_layout = html.Div(
        html.Div(
            className='columns no-print',
            children=[
                html.Div(
                    className='column',
                    children=[
                        community_selector
                    ]
                ),
                html.Div(
                    className='column',
                    children=[
                        decade_selector
                    ]
                )
            ]

        )
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
            className='help',
            id='helptext'
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
                    href='http://ckan.snap.uaf.edu/dataset/community-charts-temperature-and-precipitation'
                )
            ]
        )
    ]
)

form_layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='columns no-print',
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
* Click Inter-model Variability. Notice the black lines extending above and below each bar. The shaded bars represent the average (mean) values from all 5 models, and the black lines show the lowest and highest values among the 5 models used. Baseline years have no variability values because they are derived directly from climate station data, rather than from the 5 models.
* Click "Off" to hide variability values and show only the 5-model average.


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
                            src=path_prefix + 'assets/SNAP.svg'
                        )
                    ]
                ),
                html.A(
                    href='https://uaf.edu/uaf/',
                    target='_blank',
                    className='level-item',
                    children=[
                        html.Img(
                            src=path_prefix + 'assets/UAF.svg'
                        )
                    ]
                ),
                html.A(
                    href='https://www.gov.nt.ca/',
                    target='_blank',
                    className='level-item',
                    children=[
                        html.Img(
                            src=path_prefix + 'assets/NWT.svg'
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
                            className='columns',
                            children=[
                                html.Div(
                                    className='header--logo',
                                    children=[
                                        html.A(
                                            className='header--snap-link',
                                            href='https://snap.uaf.edu',
                                            rel='external',
                                            target='_blank',
                                            children=[
                                                html.Img(src=path_prefix + 'assets/SNAP_acronym_color_square.svg')
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
                                            'Explore temperature and precipitation projections for communities across Alaska and Western Canada.',
                                            className='subtitle is-4'
                                        )
                                    ]
                                ),
                                html.Div(
                                    className='header--map',
                                    children=[
                                        html.Div(
                                            children=[
                                                html.Img(src=path_prefix + 'assets/akcanada.svg')
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
        dcc.Graph(id='ccharts', config=config)
    ]
)


main_layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='section',
            children=[
                header_layout,
                form_layout,
                graph_layout,
                explanations
            ]
        )
    ]
)

layout = html.Div(
    children=[
        header_section,
        main_layout,
        footer
    ]
)
