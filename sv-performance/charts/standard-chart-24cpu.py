#!/usr/bin/env python3

import sys
from datetime import datetime
import pygal # pygal, library for creating svg charts
import common.chartutils as chart

column_info = \
        [{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu0:usr'    ,'column':  0, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu1:usr'    ,'column':  5, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu2:usr'    ,'column': 10, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu3:usr'    ,'column': 15, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu4:usr'    ,'column': 20, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu5:usr'    ,'column': 25, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu6:usr'    ,'column': 30, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu7:usr'    ,'column': 35, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu8:usr'    ,'column': 40, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu9:usr'    ,'column': 45, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu10usr'    ,'column': 50, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu11:usr'   ,'column': 55, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu12:usr'   ,'column': 60, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu13:usr'   ,'column': 65, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu14:usr'   ,'column': 70, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu15:usr'   ,'column': 75, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu16:usr'   ,'column': 80, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu17:usr'   ,'column': 85, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu18:usr'   ,'column': 90, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu19:usr'   ,'column': 95, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu20:usr'   ,'column': 100, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu21:usr'   ,'column': 105, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu22:usr'   ,'column': 110, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'cpu23:usr'   ,'column': 115, 'type':'value', 'max':100, 'avg':10, 'delta':0.01, 'color':'#AA0000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'load avg 1m' ,'column': 120, 'type':'value', 'max':1,   'avg':60, 'delta':0.01, 'color':'#00AA00'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'load avg 5m'  ,'column': 121, 'type':'value', 'max':1,   'avg':60, 'delta':0.01, 'color':'#00AA77'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'load avg 15m' ,'column': 122, 'type':'value', 'max':1,   'avg':60, 'delta':0.01, 'color':'#00AA33'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'memory used'  ,'column': 123, 'type':'value', 'max':32000000000, 'avg':30,'delta':0.01, 'color':'#0000AA'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'net RX'       ,'column': 127, 'type':'value', 'max':1000000, 'avg':100,'delta':0.01, 'color':'#330000'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'net TX'       ,'column': 128, 'type':'value', 'max':1000000, 'avg':100,'delta':0.01, 'color':'#FFF333'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'disk read/s'  ,'column': 133, 'type':'value', 'max':1000000, 'avg':1000,'delta':0.01, 'color':'#DD00BA'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'disk write/s' ,'column': 134, 'type':'value', 'max':1000000, 'avg':1000,'delta':0.01, 'color':'#0000BB'}
        ,{'file':'testdata/dstat24cpu.csv' ,'curvename':'time'        ,'column': 136, 'type':'x-axis'}


#        ,{'file':'testdata/bitcoind24cpu.csv'  ,'curvename':'standard txn','column':  1, 'type':'value', 'max':10000, 'avg':10, 'delta':0.01, 'color':'#000000'}
#       ,{'file':'testdata/bitcoind24cpu.csv'  ,'curvename':'getminingcandidate','column':5,'type':'event','max':1,   'avg':10, 'delta':0.01, 'color':'#666666'}
#       ,{'file':'testdata/bitcoind24cpu.csv'  ,'curvename':'submitminingsolution','column':6,'type':'timerevent','max':1,   'avg':10, 'delta':0.01, 'color':'#888888'}
#       ,{'file':'testdata/bitcoind24cpu.csv'  ,'curvename':'poolsz','column':7, 'type':'value', 'max':10000, 'avg':10, 'delta':0.01, 'color':'#555555'}
#        ,{'file':'testdata/bitcoind24cpu.csv'  ,'curvename':'time'        ,'column':  0, 'type':'x-axis'}



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
        title="chart with dstat24cpu.cp and bitcoind24cpu.log",              # patched directly into the svg file (e.g. width and height)
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
        'svg-file':'testdata/standardchart24cpu.svg'
        }

chart.render(configuration)

