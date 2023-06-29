#!/bin/bash

if test -f testdata/data.svg; then
	rm testdata/data.svg
fi

testdata/create-example-csv.py > testdata/data.csv
testdata/create-example-log.py > testdata/event.log
cat testdata/event.log | testdata/csv-from-example-log.py > testdata/event.csv
./example-chart.py

if test -f testdata/data.svg; then
	firefox testdata/data.svg&
fi
