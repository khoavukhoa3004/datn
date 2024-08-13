# syntax=docker/dockerfile:1

# FROM python:3.8-slim-buster
# FROM python:3.8-alpine3.17
FROM ubuntu:22.04
WORKDIR /app

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update

RUN apt autoremove python
RUN apt install -y python3.10
RUN apt install -y g++
RUN apt install -y python3-pip
RUN python3 --version
COPY setup.py setup.py
RUN pip3 install --upgrade pip
RUN pip3 install --ignore-installed blinker==1.7.0
RUN pip3 install .

COPY ./config /app/config
COPY ./constants /app/constants
# COPY ./files /app/files
COPY ./response /app/response
COPY ./solution /app/solution
COPY ./templates /app/templates
COPY ./files /app/files
COPY ./files/test /app/files/test
COPY ./utils /app/utils
COPY ./flaskr /app/flaskr
# COPY ./logs /app/logs
RUN mkdir /logs
# TODO: change ./.env to ./.env.production
# COPY ./.env.production /app/.env
COPY ./.env.docker /app/.env
COPY ./gunicorn.conf.py /app/
COPY ./wsgi.py /app/
COPY ./script.sh /app/

ENTRYPOINT ["sh", "script.sh", "-p"]