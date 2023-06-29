#!/bin/bash

#kill dstat process before logrotation


kill -9 $(ps -ef | grep 'python2 /usr/bin/dstat' | grep 'root' | grep -v 'color=auto' | grep -v 'grep' | awk '{print $2;exit}')
