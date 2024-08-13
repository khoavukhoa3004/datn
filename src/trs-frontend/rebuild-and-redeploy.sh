#!/bin/sh

docker stop trs_fe;
docker rm trs_fe;
docker build --tag trs_fe .;
docker run --name trs_fe -d --net=recsys-network -p 3000:3000 \
    -v "$(pwd)"/logs:/app/logs \
    --restart always \
    trs_fe;
exit;