"""
SNAP Community Charts / Community Climate
"""
# pylint: disable=invalid-name, import-error, line-too-long, too-many-arguments

import re
import json
import copy
import os
import urllib.request
import urllib.parse
import html as h
import pandas as pd
import dash
from dash.dependencies import Input, Output
from flask import Response
import flask
import luts
from gui import layout

path_prefix = os.environ["DASH_REQUESTS_PATHNAME_PREFIX"]

data_prefix = os.environ.get("DATA_PREFIX")
if data_prefix is None:
    data_prefix = ""

app = dash.Dash(__name__)
app.title = luts.title
# AWS Elastic Beanstalk looks for application by default,
# if this variable (application) isn't set you will get a WSGI error.
application = app.server

with open("CommunityNames.json", "r") as community_file:
    communities = json.load(community_file)

Months = luts.Months

# Customize this layout to include Google Analytics
app.index_string = luts.index_string

app.layout = layout


def filter_community_id(community_id):
    """Strip invalid characters from community ID input"""
    return re.sub("[^A-Z0-9]+", "", community_id)


def full_community_name(community):
    """Combine community name with alt_name if it exists"""
    if "alt_name" in community:
        return "{0} ({1})".format(community["name"], community["alt_name"])
    return community["name"]


@app.callback(
    Output("ccharts", "figure"),
    inputs=[
        Input("community", "value"),
        Input("variable", "value"),
        Input("scenario", "value"),
        Input("units", "value"),
    ],
)
def update_graph(community_raw, variable, scenario, units):
    """Update the graph from user input"""

    # Default!
    if community_raw is None:
        community_raw = "AK124"

    community_id = filter_community_id(community_raw)
    community = communities[community_id]
    comm_file = data_prefix + "data/" + community_id + ".csv"
    df = pd.read_csv(comm_file)

    # [ML] maybe hardwire these? Not a huge time sink, but it could be made cleaner
    mean_cols = [col for col in df.columns if "Mean" in col]

    resolution_lu = luts.resolution_lu
    variable_lu = luts.variable_lu
    # subset to the data we want to display using the callback variables

    if community["region"] == "Northwest Territories":
        baseline = "cru32"
    else:
        baseline = "prism"

    dff = df[
        (df["community"] == community["name"])
        & (df["resolution"] == resolution_lu[baseline])
        & (df["type"] == variable_lu[variable])
        & (df["scenario"] == scenario)
    ]
    cols = mean_cols + ["daterange", "region"]  # fun with list appending!
    dff = dff[cols]  # grab just the cols we need
    baseline_df = df[
        (df["community"] == community["name"])
        & (df["resolution"] == resolution_lu[baseline])
        & (df["type"] == variable_lu[variable])
        & (df["scenario"] == baseline.lower())
    ]
    baseline_df = baseline_df[mean_cols]  # grab just the cols we need

    # handle units conversion if needed:
    imperial_conversion_lu = luts.imperial_conversion_lu
    if units == "imperial":
        # make things F/inches
        dff[mean_cols] = dff[mean_cols] * imperial_conversion_lu[variable]
        baseline_df[mean_cols] = (
            baseline_df[mean_cols] * imperial_conversion_lu[variable]
        )

    # scenario lookup
    scenario_lu = luts.scenario_lu
    emission_label = scenario_lu[scenario]

    # unit lookup
    unit_lu = luts.unit_lu

    # baseline lookup
    baseline_lu = luts.baseline_lu
    baseline_label = baseline_lu[baseline]

    # set the freezing line for TEMPERATURE based on imperial or metric
    tMod = 0

    # Base Layout Item (for both variables)
    figure_layout = copy.deepcopy(luts.figure_layout)

    # Include alternate community name if one exists
    community_name = full_community_name(community)

    if variable == "temp":
        if units == "imperial":
            tMod = 32
        # Lookup table for included decades (default: 2010,2040,2060,2090)
        df_lu_full_temp = luts.df_lu_full_temp
        df_lu = dict()

        for decade in luts.decades:
            df_lu[decade] = df_lu_full_temp[decade]

        figure = {
            "data": [
                {
                    "x": Months,
                    "y": baseline_df[mean_cols].iloc[0],
                    "type": "bar",
                    "base": tMod,
                    "marker": {"color": "#999999"},
                    "name": "Historical ",
                }
            ]
        }
        for key in sorted(df_lu):
            df_l = dff[dff["daterange"] == key]
            figure["data"].append(
                {
                    "x": Months,
                    "y": df_l[mean_cols].iloc[0],
                    "type": "bar",
                    "base": tMod,
                    "marker": {"color": df_lu[key]["color"]},
                    "name": key + " ",
                }
            )
        figure["layout"] = figure_layout
        figure["layout"]["title"] = (
            "<b>Average Monthly Temperature for "
            + community_name
            + ", "
            + community["region"]
            + "</b><br>Historical "
            + baseline_label
            + " and 5-Model Projected Average at "
            + resolution_lu[baseline]
            + " resolution, "
            + emission_label
            + " Scenario &nbsp;"
        )
        figure["layout"]["yaxis"] = {
            "zeroline": "false",
            "zerolinecolor": "#efefef",
            "zerolinewidth": 0.5,
            "title": "Temperature (" + unit_lu["temp"][units] + ")",
        }
        figure["layout"]["shapes"] = [
            {
                "type": "line",
                "x0": 0,
                "x1": 1,
                "xref": "paper",
                "y0": tMod,
                "y1": tMod,
                "yref": "y",
                "line": {"width": 1},
            }
        ]
        return figure

    # Lookup table for included decades (default: 2010,2040,2060,2090)
    df_lu_full_precip = luts.df_lu_full_precip
    df_lu = dict()
    for decade in luts.decades:
        df_lu[decade] = df_lu_full_precip[decade]

    figure = {
        "data": [
            {
                "x": Months,
                "y": baseline_df[mean_cols].iloc[0],
                "type": "bar",
                "marker": {"color": "#999999"},
                "name": "Historical ",
            }
        ]
    }
    for key in sorted(df_lu):
        df_l = dff[dff["daterange"] == key]
        figure["data"].append(
            {
                "x": Months,
                "y": df_l[mean_cols].iloc[0],
                "type": "bar",
                "marker": {"color": df_lu[key]["color"]},
                "name": key + " ",
            }
        )

    figure["layout"] = figure_layout
    figure["layout"]["title"] = (
        "<b>Average Monthly Precipitation for "
        + community_name
        + ", "
        + community["region"]
        + "</b><br>Historical "
        + baseline_label
        + " and 5-Model Projected Average at "
        + resolution_lu[baseline]
        + " resolution, "
        + emission_label
        + " Scenario &nbsp;"
    )
    figure["layout"]["yaxis"] = {
        "title": "Precipitation (" + unit_lu["precip"][units] + ")"
    }
    return figure


@app.callback(
    Output("download_single", "href"),
    Output("download_single", "children"),
    [Input("community", "value")],
)
def update_download_link(comm):
    """Update CSV download button target and text"""
    community_id = filter_community_id(comm)
    community = communities[community_id]
    community_name = full_community_name(community)
    url = path_prefix + "dash/dlCSV?value={}".format(community_id)
    text = "Download CSV for " + community_name + ", " + community["region"]
    return url, text


@app.server.route("/dash/dlCSV")
def download_csv():
    """Send CSV to user using full community file name"""
    value = flask.request.args.get("value")
    value = h.unescape(value)
    community_id = filter_community_id(value)
    community = communities[community_id]
    pathname = data_prefix + "data/" + community_id + ".csv"

    if data_prefix.find("http") != -1:
        with urllib.request.urlopen(pathname) as response:
            csv = response.read().decode("utf-8")
    else:
        with open(pathname, mode="r") as file_handle:
            csv = file_handle.read()

    community_name = full_community_name(community)
    community_with_region = community_name + ", " + community["region"]
    underscored_community = re.sub("[ ,]+", "_", community_with_region)
    csv_filename = urllib.parse.quote(underscored_community) + ".csv"

    return Response(
        csv,
        mimetype="text/csv",
        headers={
            "Content-disposition": "attachment; filename="
            + csv_filename
            + "; filename*=utf-8''"
            + csv_filename,
            "Content-type": "text/csv;charset=utf-8",
        },
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug = os.environ.get("DEBUG", False)
    app.run_server(debug=debug, port=port)
