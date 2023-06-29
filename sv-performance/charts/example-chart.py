#!/usr/bin/env python3

import sys
from datetime import datetime
import pygal # pygal, library for creating svg charts
import common.chartutils as chart

####################################### # CONFIGURATION #####

column_info = \
        [{'file':'testdata/data.csv',     'curvename':'sinus'           ,'column':1    ,'type':'value'      ,'max':1    ,'avg':1   ,'delta':0.01  ,'color':'#00CC00'} \
        ,{'file':'testdata/data.csv',     'curvename':'atan'            ,'column':2    ,'type':'value'      ,'max':1    ,'avg':1   ,'delta':0.01  ,'color':'#CC0000'} \
        ,{'file':'testdata/data.csv',     'curvename':'atan 0.08delta'  ,'column':2    ,'type':'value'      ,'max':1    ,'avg':1   ,'delta':0.08  ,'color':'#BB7777'} \
        ,{'file':'testdata/data.csv',     'curvename':'time'            ,'column':0    ,'type':'x-axis'} 

        ,{'file':'testdata/event.csv',    'curvename':'cos avg1'        ,'column':1    ,'type':'value'      ,'max':1000 ,'avg':1   ,'delta':0.01  ,'color':'#0000CC'} \
        ,{'file':'testdata/event.csv',    'curvename':'cos avg60'       ,'column':1    ,'type':'value'      ,'max':1000 ,'avg':60  ,'delta':0.01  ,'color':'#7777BB'} \
        ,{'file':'testdata/event.csv',    'curvename':'start event'     ,'column':2    ,'type':'event'      ,'max':1    ,'avg':0   ,'delta':0.01  ,'color':'#00BBBB'} \
        ,{'file':'testdata/event.csv',    'curvename':'stop event'      ,'column':3    ,'type':'timerevent' ,'max':1    ,'avg':0   ,'delta':0.01  ,'color':'#BBBB00'} \
        ,{'file':'testdata/event.csv',    'curvename':'time'            ,'column':0    ,'type':'x-axis'} 

        ]

custom_style = pygal.style.Style(
        colors=([c['color'] for c in column_info if c['type'] != 'x-axis']),
        font_family='Roboto,Helvetica,Arial,sans-serif',
        background='transparent',
        label_font_size=14
)

def create_chart_renderer():
    return pygal.XY(                            # pygal bug, do not set width and height.
        title="test chart",                     # We patch those directly into the svg file.
        y_title='values relative to max value in configuration',
        margin_left=0,
        margin_top=0,
        x_label_rotation=320,
        x_value_formatter= lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'),
        pretty_print=True,
        #interpolate='cubic',
        #interpolate='quadratic',
        #interpolate='hermite',
        style=custom_style
    )

configuration = {
        'xaxis-spacing':40,                     # compress x-axis more or less according to gut feeling
        'xaxis-interval': 10,                   # decorating every n-th cuve point with a label
        'xaxis-interpolationlimit': 50,         # paint a dot if no interpolation happened after this count of seconds
        'column-info':column_info,
        'chart-renderer': create_chart_renderer,
        'svg-file':'testdata/data.svg'
        }

chart.render(configuration)

