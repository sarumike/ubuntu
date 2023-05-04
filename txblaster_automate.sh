#!/bin/bash

#define conf file - name and location of bsv conf file
config=~/.bitcoin/bitcoin.conf

#define regtest folder - location of the regtest folder
regtest=~/.bitcoin

#define output folder to hold txns generated - shared container folder mapping
output=~/.bitcoin/TN

#define private keys location - location in txblaster docker container
keys=~/.bitcoin/524K_privateKeysWithPublic.txt

#define bsv binaries location
bsv=~/bitcoin-sv-1.0.9/src

#set variables for blocks and coins to send
blocks=1000
coins=14500


echo "############ read values from .conf file ###################"
echo ""

port=$(awk '/^port=/ {print substr($1,6)}' $config)
rpcport=$(awk '/^rpcport=/ {print substr($1,9)}' $config)
rpcuser=$(awk '/^rpcuser=/ {print substr($1,9)}' $config)
rpcpwd=$(awk '/^rpcpassword=/ {print substr($1,13)}' $config)


echo "Step 1: stop node if running"
$bsv/bitcoin-cli -conf=$config stop

sleep 60

echo "Step 2: remove regtest folder"

rm -r $regtest/regtest

sleep 10

echo "Step 3: start up bsv node"

$bsv/bitcoind -conf=$config -genesisactivationheight=100 -maxscriptsizepolicy=0 -excessiveblocksize=0 -maxstackmemoryusageconsensus=0  -limitancestorcount=500 -limitdescendantcount=500 -daemon
sleep 30

echo "Step 4: generate empty blocks"
$bsv/bitcoin-cli -conf=$config generate $blocks
sleep 10

echo "Step 5: grab new address"
newaddr=$($bsv/bitcoin-cli -conf=$config getnewaddress)

echo "new address is  " $newaddr

sleep 10

echo "Step 6: dump out private key from address"
dumpkey=$($bsv/bitcoin-cli -conf=$config dumpprivkey $newaddr)

echo "private key is " $dumpkey

sleep 10

echo "Step 7: send coins to address"
addr=$($bsv/bitcoin-cli -conf=$config sendtoaddress $newaddr $coins) 
sleep 10

echo "txn is " $addr

echo "Step 8: get raw txn for funding"
rawtxn=$($bsv/bitcoin-cli -conf=$config getrawtransaction $addr) 

echo "raw txn is " $rawtxn


echo "Step 9: create json file for txblaster"

echo "remove any existing generate.json file"
rm generate.json

echo "{" > generate.json
echo "\""networkType\"": \""RegTest\"", " >> generate.json
echo "\""savePathRoot\"": \""$output\""," >> generate.json
echo "\""fundingPrivateKeyWIF\"": \""$dumpkey\"", " >> generate.json
echo "\""fundingTransaction\"": \""$rawtxn\"", " >> generate.json
echo "\""numberOfInputsPerTransaction\"": 1, " >> generate.json
echo "\""numberOfOutputsPerTransaction\"": 2, " >> generate.json
echo "\""numberOfTransactionsToGenerate\"": 1000000, " >> generate.json
echo "\""maxChainLength\"": 1, " >> generate.json
echo "" >> generate.json
#echo "\""verifyRpcNodeParameters\"": {" >> generate.json
#echo "          \""rpcAddress\"":  \""127.0.0.1:$rpcport\""," >> generate.json
#echo "		\""user\"": \""$rpcuser\"", " >> generate.json
#echo "          \""password\"": \""$rpcpwd\"" " >> generate.json
#echo "	}," >> generate.json
#echo "" >> generate.json
echo "\""adaptersConfig\"": [" >> generate.json
echo "	{" >> generate.json
echo "		\""announceTransactions\"": false, " >> generate.json
echo "		\""peerDiscovery\"": \""None\"", " >> generate.json
echo "          \""connectToPeers\"": [ \""127.0.0.1:$port\"" ]" >> generate.json
echo "		}" >> generate.json
echo "	]," >> generate.json
echo "" >> generate.json
echo "\""submitLastBatch\"": false, " >> generate.json
echo "\""sessionName\"": \""_1_2_TN_\"", " >> generate.json
echo "\""logToConsole\"": true, " >> generate.json 
echo "\""privateKeysFile\"": \""$keys\"" " >> generate.json
echo "" >> generate.json
echo "}" >> generate.json

echo ""
echo "Finished!!!!"


#echo "copy generate.json file into docker container"
#container_name=$(sudo docker ps --format "{{.Names}}")

#sudo docker cp generate.json $container_name:/TxBlaster6/
