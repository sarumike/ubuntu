#!/bin/bash

# Things you may want to do first
#
# git fetch 
# git pull CORE-1173-create-performance-scripts
# git reset --hard origin/CORE-1173-create-performance-scripts
# cd charts
# scp -C 10.130.21.161:/home/thelma/patrick/upload/bitcoind8cpu.log ./testdata/
# scp -C 10.130.21.161:/home/thelma/patrick/upload/dstat8cpu.log ./testdata/
# ... or 
# cp your_own_bitcoind.log ./testdata/bitcoind8cpu.log
# cp your_own_dstat.csv ./testdata/dstat8cpu.log
# ensure dates are formatted as YYYY-MO-DD HH:MM:SS. You can use following sed command
# if the time stamp is the last column and formatted as DD-MO HH:MM:SS
# sed  -i -E 's/(..)-(..) (..:..:..)$/2020-\2-\1 \3/' my_csv_file.csv
# edit csv-from-bitcoinlog.py
# edit standard-chart-8cpu.py
# call
# firefox testdata/standardchart8cpu.svg
# after running this script

echo sorting bitcoin log ...
sort testdata/bitcoind24cpu.log > testdata/bitcoind24cpu.tmp
rm testdata/bitcoind24cpu.log
mv testdata/bitcoind24cpu.tmp testdata/bitcoind24cpu.log

echo converting bitcoin log to csv ...
cat testdata/bitcoind24cpu.log | ./csv-from-bitcoinlog.py > testdata/bitcoind24cpu.csv
echo creating charts from csv ...
./standard-chart-24cpu.py
