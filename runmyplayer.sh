#!/bin/bash
if [[ $# -ne 3 ]] ; then
    echo 'Usage: ./runmyplayer.sh COLOR TIME IP'
    exit 1
fi

python3 main.py --team "$1" --timeout "$2" --ip "$3"
