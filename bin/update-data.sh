#!/bin/bash

if [ "$1" == "--prod" ] ; then
    export DATA_ELAN_LINT="/srv/data"
    export REPOSITORY_ELAN_LINT="/srv/elan-linter"
    docker-compose up
elif [ "$1" == "--dev" ] ; then
    export DATA_ELAN_LINT="./data"
    export REPOSITORY_ELAN_LINT="./dist"
    docker-compose up
else
    echo "Usage: $0 [ --prod | --dev ]"
fi



