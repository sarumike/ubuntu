#!/usr/bin/env python3

import sys
from datetime import datetime
import pygal # pygal, library for creating svg charts
import common.chartutils as chart

column_info = \
        [{'file':'testdata/dstat8cpu.csv' ,'curvename':'cpu0:usr'    ,'column':  0, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'cpu1:usr'    ,'column':  5, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'cpu2:usr'    ,'column': 10, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'cpu3:usr'    ,'column': 15, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'cpu4:usr'    ,'column': 20, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'cpu5:usr'    ,'column': 25, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'cpu6:usr'    ,'column': 30, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'cpu7:usr'    ,'column': 35, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'load avg 1m'    ,'column': 40, 'type':'value', 'max':1,   'avg':60, 'delta':0.01, 'color':'#00AA00'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'load avg 5m'    ,'column': 41, 'type':'value', 'max':1,   'avg':60, 'delta':0.01, 'color':'#00AA77'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'load avg 15m'    ,'column': 42, 'type':'value', 'max':1,   'avg':60, 'delta':0.01, 'color':'#00AA33'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'memory used'        ,'column': 43, 'type':'value', 'max':32000000000, 'avg':30,'delta':0.01, 'color':'#0000AA'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'net RX'        ,'column': 47, 'type':'value', 'max':1000000, 'avg':100,'delta':0.01, 'color':'#330000'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'net TX'        ,'column': 48, 'type':'value', 'max':1000000, 'avg':100,'delta':0.01, 'color':'#FFF333'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'disk read/s'        ,'column': 53, 'type':'value', 'max':1000000, 'avg':1000,'delta':0.01, 'color':'#DD00BA'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'disk write/s'       ,'column': 54, 'type':'value', 'max':1000000, 'avg':1000,'delta':0.01, 'color':'#0000BB'}
        ,{'file':'testdata/dstat8cpu.csv' ,'curvename':'time'        ,'column': 56, 'type':'x-axis'}

        ,{'file':'testdata/bitcoind8cpu.csv'  ,'curvename':'standard txn','column':  1, 'type':'value', 'max':10000, 'avg':10, 'delta':0.01, 'color':'#000000'}
        ,{'file':'testdata/bitcoind8cpu.csv'  ,'curvename':'getminingcandidate','column':5,'type':'event','max':1,   'avg':10, 'delta':0.01, 'color':'#666666'}
        ,{'file':'testdata/bitcoind8cpu.csv'  ,'curvename':'submitminingsolution','column':6,'type':'timerevent','max':1,   'avg':10, 'delta':0.01, 'color':'#888888'}
        ,{'file':'testdata/bitcoind8cpu.csv'  ,'curvename':'poolsz','column':7, 'type':'value', 'max':10000, 'avg':10, 'delta':0.01, 'color':'#555555'}
        ,{'file':'testdata/bitcoind8cpu.csv'  ,'curvename':'time'        ,'column':  0, 'type':'x-axis'}
        ]

# Define the style
custom_style = pygal.style.Style(
        colors=([c['color'] for c in column_info if c['type'] != 'x-axis']),
        font_family='Roboto,Helvetica,Arial,sans-serif',
        background='transparent',
        label_font_size=14
)

def create_chart_renderer():
    return pygal.XY(                            # Some of the chart configuration values need to be
        title="chart with dstat8cpu.cp and bitoind8cpu.log",              # patched directly into the svg file (e.g. width and height)
        y_title='values relative to max value in configuration',
        margin_left=0,
        margin_top=0,
        x_label_rotation=320,
        pretty_print=True,
        style=custom_style
    )

configuration = {
        'xaxis-spacing':40,                     # compress x-axis more or less according to gut feeling
        'xaxis-interval': 10,                   # decorating every n-th cuve point with a label
        'xaxis-interpolationlimit': 1000,
        'column-info':column_info,
        'chart-renderer': create_chart_renderer,
        'svg-file':'testdata/standardchart8cpu.svg'
        }

chart.render(configuration)
