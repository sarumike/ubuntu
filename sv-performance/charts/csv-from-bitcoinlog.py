#!/usr/bin/env python3

import sys
#sys.path.insert(0, '.')
import common.logutils as log

####################################### # CONFIGURATION #####

configuration = []
configuration.append({'curvename':'standard txn','regex': r'.*p2p.*','type':'counter'})
configuration.append({'curvename':'txn inv','regex': r'.*got txn inv:.*','type':'counter'})
configuration.append({'curvename':'received getdata','regex': r'.*received getdata for:.*','type':'counter'})
configuration.append({'curvename':'Requesting tx','regex': r'.* Requesting tx .*','type':'counter'})
configuration.append({'curvename':'getminingcandidate','regex': r'.*getminingcandidate.*','type':'event'})
configuration.append({'curvename':'submitminingsolution','regex': r'.*submitminingsolution.*', 'start':'getminingcandidate','type':'event'})
configuration.append({'curvename':'orphan operation','regex': r'.*orphan.*','type':'counter'})

####################################### # READ LOG #####

if len(sys.argv) > 1:
    source_name = sys.argv[1]           # file name
else:
    source_name = None                  # or stdin

log.print_csv(configuration, source_name)
