FROM python:3.10 as builder
WORKDIR /bot

FROM python:3.10-slim
WORKDIR /bot

ENV PYTHONBUFFERED=1
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages

COPY . /bot

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
