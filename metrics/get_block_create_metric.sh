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






echo "block create info details using logfile $1"



awk '/UpdateTip:/ {print $7,substr($2,1,length($2)-7), substr($12,1,length($12)-1)}' $bitcoindlog | awk '{ split($2,a,":") && split ($3,b, ":");print $1, "start="$3, "stop="$2, "generate(secs)="((a[1]*3600)+(a[2]*60)+a[3]) - ((b[1]*3600) +(b[2]*60)+b[3]) }'

