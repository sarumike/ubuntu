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

def write_logs(funcs):
    titles = []
    data = []
    start = int(datetime.datetime(2020,12,24,8,0,0).timestamp())
    end = start + 600
    step = 0.000001

    t = float(start) - step
    while t <= end:
        t += step

        # print a distribution of event f[0] according to function f[1]
        for f in funcs:
            func = f[1]
            if func(t - start):
                timeasstring = datetime.datetime.fromtimestamp(float(t)).strftime('%Y-%m-%d %H:%M:%S.%f')
                print (timeasstring, 'this is a', f[0], 'function')

        # advance t randomly
        t += float(random.randint(1, 1000)) / 1000000.0

funcs = []

def cos(x):
    value = math.cos(x * 3.1415926 * 0.01)
    r = random.random()
    if abs(value) > r + 0.5:
        return True
    else:
        return False

funcs.append(['cos',cos])

def start_event(x):
    if random.randint (0,200000) == 0:
        return True
    else:
        return False

funcs.append(['start event',start_event])

def stop_event(x):
    return start_event(x - 10000000 + random.randint(0,10000000))

funcs.append(['stop event',stop_event])

write_logs(funcs)


