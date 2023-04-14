#!/bin/bash

set -o allexport
dos2unix .env.sh
source .env.sh
set +o allexport

docker-compose --env-file=/dev/null down
docker-compose --env-file=/dev/null up -d
