#!/bin/bash

echo "setup public keys to run commands on rmeote bsv node"
#eval 'ssh-agent'
eval ssh-agent

sleep 5

exec ssh-agent $SHELL
#sleep 5

ssh-add ~/.ssh/id_rsa
sleep 5

ssh-add -l
sleep 5

echo "done!!"

