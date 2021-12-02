# pylint: disable=C0103,E0401
"""
Common shared text strings, formatting defaults and lookup tables.
"""

gtag_id = "UA-3978613-1"

# Core page components
title = "SNAP Community Climate Charts"
description = "Explore temperature and precipitation projections for communities across Alaska and Western Canada"
url = "https://snap.uaf.edu/tools/community-charts"
twitter_preview = (
    "https://snap.uaf.edu/tools/community-charts/assets/twitter_preview.png"
)
facebook_preview = (
    "https://snap.uaf.edu/tools/community-charts/assets/facebook_preview.png"
)

index_string = f"""
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

        <!-- Twitter Card data -->
        <meta name="twitter:card" content="summary_large_image">
        <meta name="twitter:site" content="@SNAPandACCAP">
        <meta name="twitter:title" content="{title}">
        <meta name="twitter:description" content="{description}">
        <meta name="twitter:creator" content="@SNAPandACCAP">
        <meta name="twitter:image:src" content="{twitter_preview}">

        <!-- Open Graph data -->
        <meta property="og:title" content="{title}" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="{url}" />
        <meta property="og:image" content="{facebook_preview}" />
        <meta property="og:description" content="{description}" />
        <meta property="og:site_name" content="{title}" />
        <link rel="alternate" hreflang="en" href="{url}" />
        <link rel="canonical" href="{url}"/>

        <!-- Safari 15 tab bar color -->
        <meta name="theme-color" content="#8e1e23">

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
"""

Months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
decades = ["2030-2039", "2060-2069", "2090-2099"]

region_lu = {
    "Alaska": "AK",
    "Alberta": "AB",
    "British Columbia": "BC",
    "Manitoba": "MB",
    "Northwest Territories": "NT",
    "Saskatchewan": "SK",
    "Yukon": "YT",
}

resolution_lu = {"cru322": "10min", "prism": "2km"}

variable_lu = {"temp": "Temperature", "precip": "Precipitation"}

imperial_conversion_lu = {"temp": 1.8, "precip": 0.0393701}

scenario_lu = {
    "rcp45": "Low Emissions (RCP 4.5)",
    "rcp60": "Mid Emissions (RCP 6.0)",
    "rcp85": "High Emissions (RCP 8.5)",
}

unit_lu = {
    "temp": {"imperial": "&deg;F", "metric": "&deg;C"},
    "precip": {"imperial": "in", "metric": "mm"},
}

baseline_lu = {"cru322": "CRU TS 3.22", "prism": "PRISM"}

axis_configs = {
    "automargin": True,
    "showgrid": False,
    "showline": False,
    "ticks": "",
    "title": {"standoff": 20},
    "zeroline": False,
    "fixedrange": True,
}

xaxis_config = {**axis_configs, **{"tickformat": "%B %-d, %Y"}}
xaxis_config["title"]["text"] = "Month"

figure_layout = {
    "barmode": "grouped",
    "titlefont": {"family": "Open Sans"},
    "annotations": [
        {
            "x": 0.5,
            "y": -0.35,
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "text": "These plots are useful for examining possible trends over time, rather than for precisely predicting values.",
        },
        {
            "x": 0.5,
            "y": -0.43,
            "xref": "paper",
            "yref": "paper",
            "showarrow": False,
            "text": "Credit: Scenarios Network for Alaska + Arctic Planning, University of Alaska Fairbanks.",
        },
    ],
    "margin": dict(t=100, b=130),
    "xaxis": xaxis_config,
    "yaxis": axis_configs,
}

df_lu_full_temp = {
    "2030-2039": {"color": "#ffb100"},
    "2060-2069": {"color": "#ff5000"},
    "2090-2099": {"color": "#8b0000"},
}

df_lu_full_precip = {
    "2030-2039": {"color": "#63d2c1"},
    "2060-2069": {"color": "#3990a6"},
    "2090-2099": {"color": "#104e8b"},
}

dataset_radio_options = [
    {"label": " Temperature", "value": "temp"},
    {"label": " Precipitation", "value": "precip"},
]

units_radio_options = [
    {"label": " Imperial", "value": "imperial"},
    {"label": " Metric", "value": "metric"},
]

rcp_radio_options = [
    {"label": " Low Emissions (RCP4.5)", "value": "rcp45"},
    {"label": " Medium Emissions (RCP6.0)", "value": "rcp60"},
    {"label": " High Emissions (RCP8.5)", "value": "rcp85"},
]
