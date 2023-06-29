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




#calculate validation time

echo "time to count number of validation timeouts,  using logfile $1"

awk '/code 64/ {count++} END {print "number of timeouts=" count}' $bitcoindlog



