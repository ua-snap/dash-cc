# pylint: disable=C0103,E0401
"""
Common shared text strings, formatting defaults and lookup tables.
"""

import os
gtag_id = os.environ['GTAG_ID']

# Core page components
title = "SNAP Community Climate Charts"

index_string = f'''
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

Months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

region_lu = {
    'Alaska': 'AK',
    'Alberta': 'AB',
    'British Columbia': 'BC',
    'Manitoba': 'MB',
    'Northwest Territories': 'NT',
    'Saskatchewan': 'SK',
    'Yukon': 'YT'
}

resolution_lu = {
    'cru32': '10min',
    'prism': '2km'
}

variable_lu = {
    'temp': 'Temperature',
    'precip':'Precipitation'
}

imperial_conversion_lu = {
    'temp':1.8,
    'precip':0.0393701
}

scenario_lu = {
    'rcp45': 'Low Emissions (RCP 4.5)',
    'rcp60': 'Mid Emissions (RCP 6.0)',
    'rcp85': 'High Emissions (RCP 8.5)'
}

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

baseline_lu = {
    'cru32': 'CRU 3.2',
    'prism': 'PRISM'
}

figure_layout = {
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

df_lu_full_temp = {
    '2010-2019': {'color': '#ffd700'},
    '2020-2029': {'color': '#ffc400'},
    '2030-2039': {'color': '#ffb100'},
    '2040-2049': {'color': '#ff9900'},
    '2050-2059': {'color': '#ff7400'},
    '2060-2069': {'color': '#ff5000'},
    '2070-2079': {'color': '#e23300'},
    '2080-2089': {'color': '#b61900'},
    '2090-2099': {'color': '#8b0000'}
}

df_lu_ful_precip = {
    '2010-2019': {'color': '#7fffdf'},
    '2020-2029': {'color': '#71e8ca'},
    '2030-2039': {'color': '#63d2c1'},
    '2040-2049': {'color': '#55bcb8'},
    '2050-2059': {'color': '#47a6af'},
    '2060-2069': {'color': '#3990a6'},
    '2070-2079': {'color': '#2b7a9d'},
    '2080-2089': {'color': '#1d6494'},
    '2090-2099': {'color': '#104e8b'}
}