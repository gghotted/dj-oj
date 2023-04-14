#!/bin/bash

dos2unix .env.sh
source .env.sh

docker run -it --rm -d \
    -v $(PWD)/data:/var/lib/postgresql/data \
    -e POSTGRES_DB=${POSTGRES_DB} \
    -e POSTGRES_USER=${POSTGRES_USER} \
    -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
    -h postgres \
    -p 5432:5432 \
    postgres:latest