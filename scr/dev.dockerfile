FROM python:3.8 as builder
WORKDIR /bot
RUN pip install pipenv && \
    pipenv install --system

FROM python:3.8-slim
WORKDIR /bot
RUN npm install -g nodemon

ENV PYTHONBUFFERED=1

COPY . /bot

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
