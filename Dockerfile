FROM python:3.9-alpine as builder

ENV PYTHONUNBUFFERED 1

ENV BUILD_DEPS="gcc libc-dev linux-headers postgresql-dev"
RUN python3.9 -m venv /opt/venv && /opt/venv/bin/pip install -U pip && \
        apk add --update --no-cache $BUILD_DEPS

ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY app/ .

FROM python:3.9-alpine as api

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
ENV RUNTIME_DPS="libpq"
RUN apk add --update --no-cache $RUNTIME_DPS

WORKDIR /app

RUN adduser -D noone
USER noone