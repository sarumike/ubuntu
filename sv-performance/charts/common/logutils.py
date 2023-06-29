#!/usr/bin/env python3

import sys
import glob
import fileinput
import re
import time
from datetime import datetime

def init_startevents(configuration):
    startevents = {}
    for info in configuration:
        if 'start' in info.keys():
            startevents[info['start']] = []
    return startevents

time_pattern = re.compile('^(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d[.]\d\d\d\d\d\d)')

def read_one_line(sums, line, configuration, startevents, measured):
    m = time_pattern.search(line)
    if not m:
        return
    row = []
    hirestime = m.group(1)
    hirestime = datetime.strptime(hirestime, '%Y-%m-%d %H:%M:%S.%f').timestamp()
    timestamp = int(hirestime)
    timestr = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
    row.append(timestamp)
    for info in configuration:
        curvename = info['curvename']
        p = info['regex']
        m = p.match (line)

        if info['type'] == 'event':
            x = ''  # event did not happen
        else:
            x = 0  # a counter is not incremented

        if m:
            if curvename in startevents.keys():
                startevents[curvename].append(hirestime)

            if 'start' in info.keys():
                s = info['start']
                if not startevents[s]:
                    x = -1
                elif not (curvename in measured.keys()):
                    x = hirestime - startevents[s][-1]
                    measured[curvename] = len(startevents)
                elif len(startevents[s]) > measured[curvename]:
                    x = hirestime - startevents[s][-1]
                    measured[curvename] = len(startevents[s])
                else:
                    x = -1

            elif info['type'] == 'event':
                x = -1
            else:
                x = 1  # counter incremented
        row.append(x)

    if not sums:
        sums.extend(row)
        return

    stamp = sums[0]
    if timestamp == stamp:
        for i, info in enumerate(configuration):
            if info['type'] == 'event':
                if row[i + 1] != '':
                    sums[i + 1] = row[i + 1]
            else:
                sums[i + 1] += row[i + 1]
        return

    print(datetime.fromtimestamp(stamp), end='')
    for s in sums[1:]:
        print(',' + str(s), end='')
    print()

    null_valu_times = []
    if timestamp > stamp + 1:
        null_valu_times.append(datetime.fromtimestamp(stamp + 1))
    if timestamp > stamp + 2:
        null_valu_times.append(datetime.fromtimestamp(timestamp - 1))

    for t in null_valu_times:
        print(t, end='')
        for i, info in enumerate(configuration):
            if info['type'] == 'event':
                print (',', end='')
            else:
                print (',0', end='')
        print()

    sums.clear()
    sums.extend(row)

def print_titles(configuration):
    print('timestamp',end='')
    for info in configuration:
        print(',' + info['curvename'], end='')
    print()

def data_source(name):
    if name:
        return fileinput.FileInput(sys.argv[1])
    else:
        return fileinput.input()

def print_csv(configuration, source_name):
    print_titles(configuration)
    line_number = 0
    sums = []
    startevents = init_startevents(configuration)
    measured = {}

    for info in configuration:
        regex = info['regex']
        p = re.compile(regex)
        info['regex'] = p

    with data_source(source_name) as file:
        for line in file:                   # the main program loop
            line_number += 1
            if len(line) > 40:
                read_one_line(sums,line,configuration, startevents, measured)

