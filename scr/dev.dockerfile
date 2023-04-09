FROM python:3.8 as builder
WORKDIR /bot
RUN apt update -y && \
    apt upgrade -y
COPY ./app/Pipfile ./app/Pipfile.lock /bot/
RUN pip install pipenv && \
    pipenv install --system

FROM python:3.8-slim
WORKDIR /bot
RUN apt update -y && \
    apt upgrade -y && \
    apt install -y nodejs npm curl && \
    npm install -g n && \
    n stable && \
    apt purge -y nodejs npm && \
    apt autoremove -y
RUN npm install -g nodemon

ENV PYTHONBUFFERED=1

COPY . /bot

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
