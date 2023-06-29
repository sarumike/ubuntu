#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')
import common.logutils as log

####################################### # CONFIGURATION #####

configuration = []
configuration.append({'curvename':'cosinus','regex': r'.* cos .*','type':'counter'})
configuration.append({'curvename':'start event','regex': r'.* start event .*','type':'event'})
configuration.append({'curvename':'stop event','regex': r'.* stop event .*','type':'event','start':'start event'})

####################################### # READ LOG #####

if len(sys.argv) > 1:
    source_name = sys.argv[1]           # file name
else:
    source_name = None                  # or stdin

log.print_csv(configuration, source_name)
