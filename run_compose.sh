#!/bin/bash

set -o allexport
source .env.sh
set +o allexport

docker-compose --env-file=/dev/null down
docker-compose --env-file=/dev/null up -d
