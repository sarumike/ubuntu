echo Installing Node performance metrics.

if ! grep -q  .metrics.sh ~/.bashrc
then
    printf '\n# Node performance metrics\nif [[ -f ~/.metrics.sh ]] \n  ~/.metrics.sh\nfi' >> ~/.bashrc
    echo "Updating ~./.bashrc for the first time."
fi

cp ./.metrics.sh ~
chmod +x ~/.metrics.sh
~/.metrics.sh

if [ ! -d ~/bin ]
then
    echo "User bin directory does not exist. Creating.."$~"/bin".
    mkdir /bin
fi

echo "Copying metrics to local bin."
chmod +x get_*.sh
cp get_*.sh ~/bin

echo "Setting up aliases."

alias get_block_create_metric=~/bin/get_block_create_metric.sh

alias get_block_info_metric=~/bin/get_block_info_metric.sh

alias get_txns_timeouts_metric=~/bin/get_txns_timeouts_metric.sh

alias get_txns_validate_metric=~/bin/get_txns_validate_metric.sh
 
echo Done