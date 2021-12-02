"""
SNAP Community Charts / Community Climate
"""

import os
import json
from dash import dcc
from dash import html
import dash_dangerously_set_inner_html as ddsih
import luts

with open("CommunityNames.json", "r") as community_file:
    communities = json.load(community_file)

path_prefix = os.environ["DASH_REQUESTS_PATHNAME_PREFIX"]

dropdown_options = []
for key, community in communities.items():
    name = community["name"]
    region = community["region"]

    if "alt_name" in community:
        alt_name = community["alt_name"]
        community_string = "{0} ({1}), {2}".format(name, alt_name, region)
    else:
        community_string = "{0}, {1}".format(name, region)

    dropdown_options.append({"label": community_string, "value": key})

community_selector = html.Div(
    className="field",
    children=[
        html.Label(
            "Type the name of a community in the box below to get started.",
            className="label",
        ),
        html.Div(
            className="control px-0 mb-3",
            children=[
                dcc.Dropdown(
                    id="community",
                    options=dropdown_options,
                    value="AK124",
                )
            ],
        ),
    ],
)

dataset_radio = html.Div(
    className="field",
    children=[
        html.Label("Dataset", className="label"),
        html.Div(
            className="control",
            children=[
                dcc.RadioItems(
                    labelClassName="radio",
                    options=luts.dataset_radio_options,
                    id="variable",
                    value="temp",
                )
            ],
        ),
    ],
)

units_radio = html.Div(
    className="field",
    children=[
        html.Label("Units", className="label"),
        html.Div(
            className="control",
            children=[
                dcc.RadioItems(
                    labelClassName="radio",
                    options=luts.units_radio_options,
                    id="units",
                    value="imperial",
                )
            ],
        ),
    ],
)

rcp_radio = html.Div(
    className="field",
    children=[
        html.Label("Scenarios (RCPs)", className="label"),
        html.Div(
            className="control",
            children=[
                dcc.RadioItems(
                    labelClassName="radio",
                    options=luts.rcp_radio_options,
                    id="scenario",
                    value="rcp60",
                )
            ],
        ),
    ],
)

download_single_csv = html.Div(
    className="has-text-centered mb-6",
    children=[
        html.Div(
            className="control",
            children=[
                html.A(
                    "Download Single Community (CSV)",
                    className="button is-info",
                    id="download_single",
                    href="",
                )
            ],
        )
    ],
)

rcp_blurb = ddsih.DangerouslySetInnerHTML(
    """
<div class="mt-5">
    <label class="label">What are RCPs?</label>
    <p>This tool uses Representative Concentration Pathways (RCPs) to display climate scenarios. RCPs describe paths to future climates based on greenhouse gas concentrations. They represent possible climate futures (scenarios) out to the year 2100 and provide a basis for comparison. <a href="#rcp-explanation">Learn more about RCPs below.</a></p>
</div>
"""
)

form_inputs_left = html.Div(
    className="no-print column is-two-thirds", children=[community_selector, rcp_blurb]
)

form_inputs_right = html.Div(
    className="no-print column is-one-third form-inputs-right",
    children=[dataset_radio, rcp_radio, units_radio],
)

explanation_interpret = dcc.Markdown(
    """
    ## How to interpret climate outlooks for your community

    Climate systems naturally change year to year, as do the models built to simulate them. Because of that, these charts are best for examining trends over time, and not for precise predictions.
    """,
    className="mb-5",
)

explanation_key_changes = dcc.Markdown(
    """
    #### Look for key changes

    For example, higher monthly temperatures in spring and fall may be particularly interesting. Higher temperature could mean any or all of these things:

    * A longer growing season
    * A loss of ice and/or frozen ground needed for travel or food storage
    * Precipitation changes. A shift from snow to rain impacts water storage capacity and surface water availability. This tool reports precipitation in terms of rainwater equivalent, even though it could occur as rain or snow.
    * Increased fire risk. In many locations, winter temperatures are projected to increase dramatically.
    * Changes in species composition. Warmer winters may favor species that are less cold-hardy (including desirable crops and invasive species), or it may mean less snow and/or more rain-on-snow events that impact wildlife.
    * Thawing. Higher temperatures will impact permafrost and land-fast ice.
    """,
    className="mb-5",
)

explanation_rcps_anchor = html.A(id="rcp-explanation")

explanation_rcps = dcc.Markdown(
    """
    #### Scenarios (RCPs)

    This tool uses Representative Concentration Pathways (RCPs) to display climate scenarios. RCPs describe paths to future climates based on atmospheric greenhouse gas concentrations. They represent climate futures, or scenarios, extrapolated out to the year 2100, based on a range of possible future human behaviors. RCPs provide a basis for comparison and a “common language” for modelers to share their work.

    The RCP values 4.5, 6.0, and 8.5 indicate projected radiative forcing values—the difference between solar energy absorbed by Earth vs. energy radiated back to space—measured in watts per square meter. RCP X projects that in 2100 the concentration of greenhouse gases will be such that each square meter of Earth will absorb X times more solar energy than it did in 1750.

    * RCP 4.5 — “low” scenario. Assumes that new technologies and socioeconomic strategies cause emissions to peak in 2040 and radiative forcing to stabilize after 2100.
    * RCP 6.0 — “medium” scenario. Assumes that emissions peak in 2080 and radiative forcing stabilizes after 2100.
    * RCP 8.5 — “high” scenario. Emissions increase through the 21st century.
    """,
    className="mb-5",
)

explanations_download = dcc.Markdown(
    """
    #### Download Data

    All data used by this tool can be downloaded as a single CSV file from the [SNAP Data Portal](http://ckan.snap.uaf.edu/dataset/community-charts-temperature-and-precipitation).
    """,
    className="mb-5",
)

explanations = html.Div(
    className="is-size-5 content explanations-wrapper",
    children=[
        explanation_interpret,
        explanation_key_changes,
        explanation_rcps_anchor,
        explanation_rcps,
        explanations_download,
    ],
)

footer = html.Footer(
    className="footer",
    children=[
        ddsih.DangerouslySetInnerHTML(
            """
        <div class="container">
            <div class="columns">
                <div class="logos column is-one-fifth">
                    <a href="https://www.gov.nt.ca/">
                        <img src="assets/NWT.svg">
                    </a>
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
                    <p>Photo © Anne Kokko</p>
                </div>
            </div>
        </div>
        """
        )
    ],
)


header_section = ddsih.DangerouslySetInnerHTML(
    """
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
"""
)

header_section = ddsih.DangerouslySetInnerHTML(
    """
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
"""
)

intro_section = ddsih.DangerouslySetInnerHTML(
    """
    <div class="extent section">
        <div class="intro-text">
            <div class="extent-wrapper desktop">
                <img class="extent-map" src="assets/akcanada.svg" />
            </div>
            <h4 class="title is-4 mt-3 mb-5">What’s up — or down — in your corner&nbsp;of&nbsp;the&nbsp;North?</h4>
            <p class="my-3">See temperature and precipitation projections through 2099 for over 3,800 communities in Alaska&nbsp;and&nbsp;western&nbsp;Canada.</p>
            <p class="my-3">These projections show only patterns and trends. Look for&nbsp;changes&nbsp;like&nbsp;these:</p>
            <p class="my-3">Higher temperatures in spring and fall could mean a longer growing season and/or a shift from&nbsp;snow&nbsp;to&nbsp;rain.</p>
            <p class="my-3">Warmer, drier spring weather may&nbsp;increase&nbsp;fire&nbsp;risk.</p>
            <h5 class="title is-5 mt-5">Happy exploring!</h5>
            <div class="extent-wrapper mobile">
                <img class="extent-map" src="assets/akcanada.svg" />
            </div>
        </div>
    </div>
"""
)

config = {
    "toImageButtonOptions": {
        "title": "Export to PNG",
        "format": "png",
        "filename": "CommunityChart",
        "height": 600,
        "width": 1600,
        "scale": 1,
    },
    "modeBarButtonsToRemove": [
        "zoom",
        "zoomIn",
        "zoomOut",
        "resetScale",
        "autoScale",
        "sendToCloud",
        "pan",
        "select",
        "lasso",
        "toggleSpikeLines",
    ],
    "displayModeBar": True,
    "displaylogo": False,
}

camera_icon_text = ddsih.DangerouslySetInnerHTML(
    """
<p class="content camera-icon is-size-5 has-text-centered has-text-grey mb-1">Click the <span>
<svg viewBox="0 0 1000 1000" class="icon" height="1em" width="1em"><path d="m500 450c-83 0-150-67-150-150 0-83 67-150 150-150 83 0 150 67 150 150 0 83-67 150-150 150z m400 150h-120c-16 0-34 13-39 29l-31 93c-6 15-23 28-40 28h-340c-16 0-34-13-39-28l-31-94c-6-15-23-28-40-28h-120c-55 0-100-45-100-100v-450c0-55 45-100 100-100h800c55 0 100 45 100 100v450c0 55-45 100-100 100z m-400-550c-138 0-250 112-250 250 0 138 112 250 250 250 138 0 250-112 250-250 0-138-112-250-250-250z m365 380c-19 0-35 16-35 35 0 19 16 35 35 35 19 0 35-16 35-35 0-19-16-35-35-35z" transform="matrix(1 0 0 -1 0 850)"></path></svg>
</span> icon in the upper-right of the chart download it.</p>
"""
)

graph_layout = html.Div(
    className="container", children=[dcc.Graph(id="ccharts", config=config)]
)

form_container = html.Div(
    className="form-input section",
    children=[
        html.Div(
            className="container top",
            children=[
                html.Div(
                    className="columns controls-wrapper", children=[form_inputs_left, form_inputs_right]
                )
            ],
        )
    ],
)

bottom_container = html.Div(
    className="bottom mb-6",
    children=[
        html.Div(
            className="section",
            children=[
                camera_icon_text,
                graph_layout,
                download_single_csv,
                explanations,
            ],
        )
    ],
)

layout = html.Div(
    children=[header_section, intro_section, form_container, bottom_container, footer]
)
