FROM python:3.8 as builder
WORKDIR /bot
RUN apt install pipenv && \
    pipenv install --system

FROM python:3.8-slim
WORKDIR /bot
RUN npm install -g nodemon

ENV PYTHONBUFFERED=1

COPY . /bot

RUN apt install -r requirements.txt
