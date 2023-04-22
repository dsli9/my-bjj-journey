#!/bin/bash

# This script runs a local instance of the service using the built docker image.
# It will use the current project version as the image tag. The project should be built
# locally before attempting to run this script.

# Usage:
#   ./docker/run_locally.sh <tier> <operation>

set -euo pipefail

PROJECT_VERSION=$(poetry version -s)
GCLOUD_REGION=us-east1
GCLOUD_PROJECT_ID=bjj-dashboard-383320
GCLOUD_REPO_ID=bjj-docker-repo
DOCKER_REGISTRY=${GCLOUD_REGION}-docker.pkg.dev/${GCLOUD_PROJECT_ID}/${GCLOUD_REPO_ID}

TIER="${1}"
OPERATION="${2}"

# Somewhat hacky way to make sure we don't use localhost when running on dev since
# in the dev .env file, the host is set to localhost. When running processes on
# dev via docker, host should be set to name of DB service specified in
# docker-compose.yml. Additionally, port should be set back to default port 5432.
# The prod database also uses the default port, but if that changes, there would
# need to be an additional adjustment here.
ENV_FILE=~/projects/my-bjj-journey/secrets.${TIER}.env
DB_HOST=bjj-dev-db
DB_PORT=5432
if [[ "${TIER}" == "prod" ]]; then
    DB_HOST=$(head -1 ${ENV_FILE} | cut -d "=" -f2)
fi

echo "TIER is ${TIER}"
echo "OPERATION is ${OPERATION}"
echo "DOCKER_REGISTRY is ${DOCKER_REGISTRY}"

docker-compose up -d

# ensures that database has been spun up before doing docker run
sleep 5

# BJJ_DB_HOST and BJJ_DB_PORT env vars are set after the env file to
# overwite same vars from env file.
docker run --rm \
    --volume ~/.config/gspread:/root/.config/gspread \
    --network my-bjj-journey_default \
    --name bjj-journey \
    --env "TIER=${TIER}" \
    --env "OPERATION=${OPERATION}" \
    --env-file ${ENV_FILE} \
    --env "BJJ_DB_HOST=${DB_HOST}" \
    --env "BJJ_DB_PORT=${DB_PORT}" \
    -it ${DOCKER_REGISTRY}/bjj-journey:${PROJECT_VERSION}
