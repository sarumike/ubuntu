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
# edit csv-from-bitcoinlog.py
# edit standard-chart-8cpu.py
# call
# firefox testdata/standardchart8cpu.svg
# after running this script

echo sorting bitcoin log ...
sort testdata/bitcoind8cpu.log > testdata/bitcoind8cpu.tmp
rm testdata/bitcoind8cpu.log
mv testdata/bitcoind8cpu.tmp testdata/bitcoind8cpu.log

echo converting bitcoin log to csv ...
cat testdata/bitcoind8cpu.log | ./csv-from-bitcoinlog.py > testdata/bitcoind8cpu.csv
echo creating charts from csv ...
./standard-chart-8cpu.py
