#!/bin/bash

# dimiourgei ena diktio gia asfali epikoinwnia
docker network create app-network

# ekkinei to docker container tis mongo
docker run -d --name mongo \
  --network app-network \
  -v mongo-data:/data/db \
  -p 27017:27017 \
  mongo

# ekeini to docker container tou api server
docker run -d --name api \
  --network app-network \
  -e MONGO_URI=mongodb://mongo:27017 \
  -p 8000:8000 \
  restful-service

echo "Backend services started successfully."