#!/bin/bash

# This script is used to validate the TIER environment variable for commands that
# require the variable.

# At the moment, the script is mostly used for processes that require a connection
# to a database. The dev tier should enable a connection to a dev database, while
# the prod tier should enable a connection to a prod database.

set -eo pipefail

if [[ -z "${TIER}" ]]
    then
        echo "TIER environment variable must be provided"
        exit 1
elif [[ "${TIER}" != "dev" && "${TIER}" != "prod" ]]
    then
        echo "${TIER} is not a valid tier. Should be either 'dev' or 'prod'"
        exit 1
else
    echo "TIER: ${TIER}"
fi
