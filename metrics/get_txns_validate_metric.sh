#!/bin/bash


#assign cmd line params to variables 
num=$1
bitcoindlog=$2


# output error message if no parameters supplied

if [[ $# -eq 0 ]] ; then
    echo 'ERROR!'
    echo 'please use the following format:'
    echo 'script.sh number_of_txns logfile_name'
    exit 0
fi




#calculate validation time

echo "time to validate "$1" txns,  using logfile $2"

awk '/poolsz 1 txn/{txn1=$2;next} /poolsz '"$num"' txn/{print txn1 " " $2}' $bitcoindlog | awk '{ split($2,a,":") && split ($1,b, ":") ;print "start="$1, "finish="$2, "validationtime="((a[1]*3600)+(a[2]*60)+a[3]) - ((b[1]*3600)+(b[2]*60)+b[3]) }'

