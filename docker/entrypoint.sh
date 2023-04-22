#!/bin/bash

# Entrypoint script for docker container. Commands get run based on the OPERATION
# environment variable.

set -eo pipefail

APPLICATION_DIRECTORY=$1
DEFAULT_TIER=dev
cd "${APPLICATION_DIRECTORY}"

# TIER is optionally passed in the environment
if [[ -z "${TIER}" ]]; then
    echo "No TIER environment variable provided. Setting to 'dev' by default."
    TIER="${DEFAULT_TIER}"
elif [[ "${TIER}" != "dev" && "${TIER}" != "prod" ]]; then
    echo "${TIER} is not a valid tier. Should be either 'dev' or 'prod'"
    exit 1
fi

# OPERATION should be passed in the environment
if [[ "${OPERATION}" == "data-pipeline" ]]; then
    echo "Running python data pipeline."
    poetry run python -m bjj_journey.data_pipeline -v
elif [[ "${OPERATION}" == "migrations" ]]; then
    echo "Running migrations via alembic"
    poetry run alembic upgrade head
elif [[ "${OPERATION}" == "dbt" ]]; then
    echo "Running dbt"
    poetry run dbt run --project-dir dbt --target "${TIER}"
else
    echo "${OPERATION} is not a valid operation."
    exit 1
fi
