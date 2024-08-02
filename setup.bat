#!/bin/bash

#dimiourgei tin eikona gia tin rest ipiresia
docker build -t restful-service .

# dimiourgei xwro gia tin apothikeusi tis vasis
docker volume create mongo-data

echo "Setup completed successfully."