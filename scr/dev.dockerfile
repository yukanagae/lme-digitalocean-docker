FROM python:3.10 as builder
WORKDIR /bot

FROM python:3.10-slim
WORKDIR /bot

ENV PYTHONBUFFERED=1

COPY . /bot

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
