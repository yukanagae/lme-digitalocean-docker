FROM python:3.10 as builder


FROM python:3.10-slim

ENV PYTHONBUFFERED=1

COPY . /bot

RUN python -m pip install --upgrade pip
RUN python -m pip install -r ./requirements.txt
