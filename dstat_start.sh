#!/bin/bash


#exec 5> dstat_output.txt
#BASH_XTRACEFD="5"

# startup dstat after logrotation

dstat --cpu -C all -lmnp --top-cpu -d --top-mem -t --output dstat.csv &>/dev/null &