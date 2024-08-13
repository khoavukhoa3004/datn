#!/bin/sh

docker stop RecSys-Backend-core;
docker rm RecSys-Backend-core;
docker build --tag recsys-backend-core .;
docker run --name RecSys-Backend-core -d --net=recsys-network -p 5002:5002 \
    -v "$(pwd)"/logs:/app/logs \
    -v "$(pwd)"/files:/app/files \
    -v "$(pwd)"/files/test:/app/files/test \
    -v "$(pwd)"/solution:/app/solution \
    --restart always \
    recsys-backend-core;
exit;