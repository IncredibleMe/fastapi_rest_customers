#!/bin/bash

# Stamataei ta container
docker stop api mongo
docker rm api mongo

# Diagrafei to diktio
docker network rm app-network

# Diagrafei ta dedomena tis vasis
# docker volume rm mongo-data

echo "Backend services stopped and cleaned up."