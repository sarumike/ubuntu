if [ -d ~/bin ]
then
    echo Uninstalling node performance metrics.

    #rm ~/bin/install_metrics.sh
    #rm ~/bin/uninstall_metrics.sh
    if [[ -f ~/.metrics.sh ]]
    then
        rm ~/.metrics.sh 
    fi
    if [[ -f ~/.metrics.sh ]]
    then
        rm ~/bin/get_*.sh 
    fi

    alias get_block_create_metric=
    alias get_block_info_metric=
    alias get_txns_timeouts_metric=
    alias get_txns_validate_metric=
fi 