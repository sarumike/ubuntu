#!/usr/bin/env python3

#import sys
#import glob
import fileinput
import re
#import time
#import gc
#import copy
#import pygal  # pygal, library for creating svg charts
#from pygal.style import Style  # with support for css configuration
from datetime import datetime

def get_xaxis_time(time_as_string):             # honour the column format in the csv data file
    return datetime.strptime(time_as_string, '%Y-%m-%d %H:%M:%S').timestamp()


# reads one line of csv data
def read_row(curves, configuration, line, line_number, filename):
    values = re.split(r',', line.strip('\n').strip('\r').strip('"'))
    curve_infos = [c for c in configuration['column-info'] if c['file'] == filename]
    new_curve_points = {}

    # get the x value
    for info in curve_infos:
        if info['type'] == 'x-axis':
            colindex = info['column']
            value = values[colindex]
            try:
                x = get_xaxis_time(value)
            except:
                print("non time formatted tring in file", filename,
                      "line", line_number,
                      "column", info['curvename'], ":", value)
                return
            break

    # the the y value s
    for info in curve_infos:
        if info['type'] != 'x-axis':
            colindex = info['column']
            value = values[colindex]
            normalise = info['max']  # we use potential max to normalise
            curvename = info['curvename']

            try:
                if value != None and value != '':
                    y = float(value)
                    if y != 0:
                        y = float(y) / float(normalise)
                    else:
                        y = 0.0
                    new_curve_points[curvename] = y

            except:
                print("non float value in file", filename,
                      "line", line_number,
                      "column", curvename, ":", value)
                return

    for curvename, y in new_curve_points.items():
        if not curvename in curves.keys():
            curves[curvename] = []
        curves[curvename].append([x, y])

def calculate_xaxis_values(curves, configuration):
    start = None
    end = None
    for _, curve in curves.items():
        for x,y in curve:
            if start == None or x < start:
                start = x
            if end == None or x > end:
                end = x

    assert (start)
    assert (end)

    frequency = configuration['xaxis-interval']

    while start % frequency != 0:
        start -= 1
    while end % frequency != 0:
        end += 1

    return [{
        'label': datetime.fromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'),
        'value': float(x)
    } for x in range(int(start), int(end), frequency)]

def is_interpolatable(v1, v2, v3, t1, t2, t3, delta):
    x = (t2 - t1) * (v3 - v1) / (t3 - t1)
    if abs((v1 + x) - v2) < delta:
        return True
    else:
        return False

def interpolate_curve_points(curves, configuration):
    column_infos = configuration['column-info']
    xaxis_interpolationlimit = configuration['xaxis-interpolationlimit']

    for curvename, col in curves.items():
        info = [x for x in column_infos if x['curvename'] == curvename][0]
        if info['type'] in ['value']:
            delta = info['delta']
            r1 = 0
            while r1 < len(col) - 2:
                t1 = col[r1][0]
                v1 = col[r1][1]
                r3 = r1 + 2
                r3_last = r1 + 1
                while r3 < len(col):
                    t3 = col[r3][0]
                    v3 = col[r3][1]
                    curve_point_included = False
                    for r2 in range(r1 + 1, r3):
                        t2 = col[r2][0]
                        v2 = col[r2][1]
                        interpolation = is_interpolatable(v1, v2, v3, t1, t2, t3, delta)
                        if t3 - t1 > xaxis_interpolationlimit or not interpolation or r3 == len(col) - 1:
                            t = col[r3_last][0]
                            v = col[r3_last][1]
                            for x in reversed(range(r1 + 1, r3_last - 1)):
                                del col[x]
                            curve_point_included = True
                            break

                    if curve_point_included:
                        r1 = r1 + 1
                        break
                    r3_last = r3
                    r3 += 1

def average_curve_points(curves, configuration):
    curve_infos = configuration['column-info']
    for info in curve_infos:
        if info['type'] in ['value']:
            g = info['avg']
            curvename = info['curvename']
            curve = curves[curvename]

            for i in reversed(range(len(curve))):
                avg = 0
                stop = curve[i][0] - g
                counter = 0
                ii = i
                while ii >= 0 and curve[ii][0] >= stop:
                    counter += 1
                    avg += curve[ii][1]
                    ii -= 1

                avg /= counter
                curve[i][1] = avg

class indexsequence:
    def __init__(self):
        self.counter = 0
    def get(self):
        return self.counter
    def get_and_advance(self):
        self.counter += 1
        return self.counter - 1

def render_svg_chart(curves, labels, real_width, real_height, configuration):
    svg_file = configuration['svg-file']
    column_infos = configuration['column-info']
    r = configuration['chart-renderer']()

    tipcounter = -1
    curvecounter = -1
    real_values = {}
    # not iterating over curves to get the same sqeunece as the curve_info configuration
    # otherwise the colors will not be correct

    for info in [info for info in column_infos if info['type'] != 'x-axis']:
        curvename = info['curvename']
        curvetype = info['type']
        factor = info['max']
        # A curve may be configured but not exist due to missing data points
        if not curvename in curves:
            print ("no data for curve: '{}'".format(curvename))
            continue
        curve = curves[curvename]
        curvecounter += 1
        real_values[curvename] = []
        new_curve = []
        if curvetype in ['event', 'timerevent']:

            tipcounter += 1
            for xy in curve:
                x = xy[0]
                y = xy[1]
                assert(y != None and y != 0.0)

                if curvetype == 'event':
                    new_curve.append([x, 1.0 + 0.05 * float(curvecounter)])
                    real_values[curvename].append([x, ''])
                else:
                    if y == -1:
                        new_curve.append([x, None])
                        #real_values[curvename].append([x, 'b' + str(len(new_curve))])
                        new_curve.append([x, 1.0 + 0.05 * float(curvecounter)])
                        real_values[curvename].append([x, ''])
                    else:
                        elapsed = y
                        starttime = x - elapsed

                        # null point to interrupt the curve line
                        new_curve.append([starttime, None])
                        #real_values[curvename].append([starttime, 'd'])

                        # start time arrow
                        new_curve.append([starttime, 1.0 + 0.05 * float(curvecounter)])
                        real_values[curvename].append([starttime, '123xxx123'])  # marker to remove in svg

                        # end time arrow
                        new_curve.append([x, 1.0 + 0.05 * float(curvecounter)])
                        real_values[curvename].append([x, ' -> {:.3f}sec'.format(elapsed)])

            #assert(len(new_curve) == len(real_values[curvename]))

            # Without intermediate varialbe cc pygal will break occasionally showing the lable for a different curve.
            # Also we need to show the real value and not the normalized value in the tooltip.
            # We use a lambda for that. Unfortunately this will break the x-value display in the tooltip
            # and there is unfortunately now workarround. The lambda takes only one argument

            # the default lambda parameters are required to overcome the limitation of the lexically scoped capturing

            xgenerator = indexsequence()
            ll = lambda x, curvename=curvename, xgenerator=xgenerator, real_values=real_values: '{}@{} {}'.format (
                    curvename, 
                    datetime.fromtimestamp(real_values[curvename][xgenerator.get()][0]).strftime("%H:%M:%S"),
                    real_values[curvename][xgenerator.get_and_advance()][1]
            )

            if curvetype == 'timerevent':
                r.add(curvename, new_curve, formatter=ll, dots_size=10, allow_interruptions=True,
                      stroke_style={'width': 4, 'dasharray': '1, 6', 'linecap': 'round', 'linejoin': 'round'})
            else:
                r.add(curvename, new_curve, formatter=ll, dots_size=10, stroke=False)
        else:
            r.add(curvename, curve, dots_size=2, formatter=lambda x: '{}'.format(factor * x[1]))

    r.x_labels = labels
    r.width = real_width
    r.height = real_height
    r.render_to_file(svg_file)


def patch_width_height_in_svg(real_width, real_height, configuration):
    svg_file = configuration['svg-file']

    buffer = []
    with fileinput.FileInput(svg_file, inplace=True) as file:
        for line in file:
            line = line.replace('viewBox="0 0 {0} {1}"'.format(real_width, real_height),
                                'width="{0}" height="{1}" viewBox="0 0 {0} {1}"'.format(real_width, real_height))
            buffer.append(line)
            print(line, end='')

    p1 = re.compile(r'\s*<g class="dots"')
    p2 = re.compile(r'\s*<circle')
    p3 = re.compile(r'\s*<desc.*?123xxx123')
    px = re.compile(r'\s*</g>')
    with open(svg_file, 'w') as output:
        while len(buffer) > 0:
            if len(buffer) > 3 and p1.match(buffer[0]) and p2.match(buffer[1]) and p3.match(buffer[2]):
                del buffer[0]
                del buffer[0]
                del buffer[0]
                while buffer and not px.match(buffer[0]):
                    del buffer[0]
                    assert(buffer)
                del buffer[0]
            else:
                output.write(buffer[0])
                del buffer[0]

def read_files(configuration):
    xaxis_start = None
    xaxis_end = None
    filenames = [c['file'] for c in configuration['column-info'] if c['type'] == 'x-axis']

    curves = {}
    for filename in filenames:
        with fileinput.FileInput(filename) as file:
            line_number = 0
            for line in file:  # the main program loop
                line_number += 1
                if len(line) > 10:
                    read_row(curves, configuration, line, line_number, filename)

    return curves

def render(configuration):
    curves = read_files(configuration)
    labels = calculate_xaxis_values(curves, configuration)
    average_curve_points (curves, configuration)
    interpolate_curve_points (curves, configuration)
    real_width = configuration['xaxis-spacing'] * len(labels)   # educated guess for width
    real_height = 1200                                          # fixed height optimised for HD laptop
    render_svg_chart (curves, labels, real_width, real_height, configuration)
    patch_width_height_in_svg(real_width, real_height, configuration)
