"""
SNAP Community Charts / Community Climate
"""

import os
from dash import dcc
from dash import html
import json
import dash_dangerously_set_inner_html as ddsih
import luts

df = None

with open('CommunityNames.json', 'r') as community_file:
    communities = json.load(community_file)

path_prefix = os.environ['DASH_REQUESTS_PATHNAME_PREFIX']


community_selector = html.Div(
    className='field',
    children=[
        html.Label('Type the name of a community in the box below to get started.', className='label has-text-centered'),
        html.Div(
            className='control column px-0 mb-3 community-selector',
            children=[
                dcc.Dropdown(
                    id='community',
                    options=[{'label':name, 'value':id} for id, name in communities.items()],
                    value='AK124'
                )
            ]
        )
    ]
)

community_selector_layout = html.Div(
        html.Div(
            className='no-print',
            children=[
                community_selector
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
                    options=luts.dataset_radio_options,
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
                    options=luts.units_radio_options,
                    id='units',
                    value='imperial'
                )
            ]
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
                    options=luts.rcp_radio_options,
                    id='scenario',
                    value='rcp60'
                )
            ]
        )
    ]
)

download_single_csv = html.Div(
    className='has-text-centered mb-6',
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

radio_buttons_left = html.Div(
    className='column is-one-third',
    children=[
        html.Div(
            children=[
                dataset_radio
            ]
        )
    ]
)

radio_buttons_middle = html.Div(
    className='column is-one-third',
    children=[
        html.Div(
            children=[
                units_radio
            ]
        )
    ]
)

radio_buttons_right = html.Div(
    className='column is-one-third',
    children=[
        html.Div(
            children=[
                rcp_radio
            ]
        )
    ]
)

radio_button_layout = html.Div(
    className='container',
    children=[
        html.Div(
            className='columns no-print',
            children=[
                radio_buttons_left,
                radio_buttons_middle,
                radio_buttons_right
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

###### More details
* [SNAP’s model evaluation and selection process](https://www.snap.uaf.edu/methods/model-selection)
* [General Circulation Models and Global Climate Models](https://www.sciencedaily.com/terms/global_climate_model.htm)

#### Download Data

All data used by this tool can be downloaded as a single CSV file from the [SNAP Data Portal](http://ckan.snap.uaf.edu/dataset/community-charts-temperature-and-precipitation).

""",
            className='is-size-5 content'
        )
    ]
)


footer = html.Footer(
    className='footer',
    children=[
        ddsih.DangerouslySetInnerHTML(f"""
        <div class="container">
            <div class="columns">
                <div class="logos column is-one-fifth">
                    <br>
                    <a href="https://uaf.edu/uaf/">
                        <img src="assets/UAF.svg">
                    </a>
                </div>
                <div class="column content is-size-5">
                    <p>This tool is part of an ongoing collaboration between the <a href="https://uaf-snap.org">Scenarios Network for Alaska + Arctic Planning</a> and the Government of Northwest Territories. We are working to make a wide range of downscaled climate products that are easily accessible, flexibly usable, and fully interpreted and understandable to users in the Northwest Territories, while making these products relevant at a broad geographic scale.
                    </p>
                    <p>Please contact <a href="mailto:uaf-snap-data-tools@alaska.edu">uaf-snap-data-tools@alaska.edu</a> if you have questions or would like to provide feedback for this tool. <a href="https://uaf-snap.org/tools-overview/">Visit the SNAP Climate + Weather Tools page</a> to see our full suite of interactive web tools.</p>
                    <p>Copyright © 2021 University of Alaska Fairbanks.  All rights reserved.</p>
                    <p>UA is an AA/EO employer and educational institution and prohibits illegal discrimination against any individual.  <a href="https://www.alaska.edu/nondiscrimination/">Statement of Nondiscrimination</a> and <a href="https://www.alaska.edu/records/records/compliance/gdpr/ua-privacy-statement/">Privacy Statement</a>.</p>
                    <p>Photo © __________</p>
                </div>
            </div>
        </div>
        """)
    ]
)


header_section = ddsih.DangerouslySetInnerHTML(f"""
<div class="header">
    <div class="page-bar">
        <div class="page-bar-container container">
            <div class="page-bar-row has-text-centered">
                UNIVERSITY OF ALASKA FAIRBANKS&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;SCENARIOS NETWORK FOR ALASKA + ARCTIC PLANNING
            </div>
        </div>
    </div>
    <div class="container">
        <div class="section">
                <div class="header--titles has-text-centered">
                    <h1 class="title is-1">Community Climate Charts</h1>
                </div>
            </div>
        </div>
    </div>
</div>
""")

header_section = ddsih.DangerouslySetInnerHTML(f"""
<div class="header">
    <div class="page-bar">
        <div class="page-bar-container container">
            <div class="page-bar-row has-text-centered">
                UNIVERSITY OF ALASKA FAIRBANKS&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;SCENARIOS NETWORK FOR ALASKA + ARCTIC PLANNING
            </div>
        </div>
    </div>
    <div class="container">
        <div class="section">
                <div class="header--titles has-text-centered">
                    <h1 class="title is-1">Community Climate Charts</h1>
                </div>
            </div>
        </div>
    </div>
</div>
""")

intro_section = ddsih.DangerouslySetInnerHTML(f"""
    <div class="section">
        <div class="intro-text">
            <div class="extent-wrapper desktop">
                <img class="extent-map" src="assets/akcanada.svg" />
            </div>
            <h4 class="title is-4 mt-3 mb-5">What’s up — or down — in your <br class="line-break show-above-1000 show-above-800-below-1215" /> corner of the North?</h4>
            <p class="my-3">See temperature and precipitation projections <br class="line-break show-above-916-below-1215" /> through 2099 for over 3,800 communities in <br class="line-break show-above-916-below-1215" /> Alaska and western Canada.</p>
            <p class="my-3">These projections show only patterns <br class="line-break show-below-800" /> and trends. <br class="line-break show-above-950 show-above-1000" /> Look for changes like these:</p>
            <p class="my-3">Higher temperatures in spring and fall <br class="line-break show-above-1000 show-above-800-below-1215" /> could mean a longer growing season <br class="line-break show-above-800-below-1215" /> and/or a shift from snow to rain.</p>
            <p class="my-3">Warmer, drier spring weather <br class="line-break show-above-1000 show-above-800-below-1215" /> may increase fire risk.</p>
            <h5 class="title is-5 mt-5">Happy exploring!</h5>
            <div class="extent-wrapper mobile">
                <img class="extent-map" src="assets/akcanada.svg" />
            </div>
        </div>
    </div>
""")

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
        'zoom',
        'zoomIn',
        'zoomOut',
        'resetScale',
        'autoScale',
        'sendToCloud',
        'pan',
        'select',
        'lasso',
        'toggleSpikeLines'
    ],
    'displayModeBar': True,
    'displaylogo': False
}

camera_icon_text = ddsih.DangerouslySetInnerHTML(f"""
<p class="content camera-icon is-size-5 has-text-centered has-text-grey mb-1">Click the <span>
<svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg>
</span> icon in the upper-right of the chart download it.</p>
""")

graph_layout = html.Div(
    className='container',
    children=[
        dcc.Graph(id='ccharts', config=config)
    ]
)

community_selector_container = html.Div(
    className='container top',
    children=[
        html.Div(
            children=[
                community_selector_layout,
            ]
        )
    ]
)

radio_button_container = html.Div(
    className='container middle',
    children=[
        html.Div(
            children=[
                radio_button_layout,
            ]
        )
    ]
)

bottom_container = html.Div(
    className='container bottom mb-6',
    children=[
        html.Div(
            className='section',
            children=[
                camera_icon_text,
                graph_layout,
                download_single_csv,
                explanations
            ]
        )
    ]
)

layout = html.Div(
    children=[
        header_section,
        intro_section,
        community_selector_container,
        radio_button_container,
        bottom_container,
        footer
    ]
)
