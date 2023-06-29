#!/usr/bin/env python3

import sys
import glob
import fileinput
import re
import time
import math
import datetime
import random

random.seed(2)

def random_skip(percentage):
    r = random.randint(0,100)
    if r <= percentage:
        return True
    else:
        return False

def createcurves(funcs):
    titles = []
    data = []
    start = int(datetime.datetime(2020,12,24,8,0,0).timestamp())
    end = start + 600

    titles.append('time')
    for t in funcs:
        titles.append(t[0])

    for t in range (start, end):
        #timeasstring = datetime.datetime.fromtimestamp(float(t) + (random.randint(0,1000000) / 1000000.0)).strftime('%Y-%m-%d %H:%M:%S.%f')
        timeasstring = datetime.datetime.fromtimestamp(float(t)).strftime('%Y-%m-%d %H:%M:%S')
        row = [timeasstring]
        skip = True
        for f in funcs:
            func = f[1]
            value = func(float(t - start))
            row.append(value)
            if value or value == 0:
                skip = False
        if not skip:
            data.append(row)

    return data, titles

funcs = []

def sinus(x):
    if not random_skip(80):
        return  math.sin(x * 3.1415926 * 0.01)
    else:
        return ""
funcs.append(['sinus',sinus])

def atan(x):
    if not random_skip(60):
        return  math.atan(x * 3.1415926 * 0.01)
    else:
        return ""
funcs.append(['atan',atan])

data,titles = createcurves(funcs)

print(','.join(titles))

for row in data:
    print(','.join([str(x) for x in row]))

