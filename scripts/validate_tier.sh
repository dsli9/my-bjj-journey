#!/bin/bash

# This script is used to validate the TIER environment variable that is set before
# running a given command. If no TIER environment variable is present, then
# TIER will be set to 'dev' by default.

# At the moment, the script is mostly used for processes that require a connection
# to a database. The dev tier should enable a connection to a dev database, while
# the prod tier should enable a connection to a prod database.

# The script takes one positional argument:
#   - cmd: the command we want to run after validating the TIER env variable.

CMD="${1}"

if [[ -z "${TIER}" ]];
    then
        echo "No TIER environment variable provided. Setting to 'dev' by default."
        TIER=dev ${CMD}
elif [[ "${TIER}" != "dev" && "${TIER}" != "prod" ]]
    then
        echo "${TIER} is not a valid tier. Should be either 'dev' or 'prod'"
        exit 1
else
    echo "TIER: ${TIER}"
    TIER="${TIER}" ${CMD}
fi
