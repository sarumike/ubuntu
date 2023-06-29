#!/bin/bash


#assign cmd line params to variables 

bitcoindlog=$1


# output error message if no parameters supplied

if [[ $# -eq 0 ]] ; then
    echo 'ERROR!'
    echo 'please use the following format:'
    echo 'script.sh logfile_name'
    exit 0
fi






echo "block info details using logfile $1"

awk '/CreateNewBlock/ {a=$2;b=$7;c=$9}  /UpdateTip/ {print $7, "time="a, "blocksize="b, "txns="c}' $bitcoindlog


