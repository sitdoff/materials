FROM python:3.12.1-alpine

LABEL creator="Roman Ivanov"
LABEL email="sitdoff@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/

RUN apk update && \
    apk add --no-cache python3-dev \
    gcc \
    musl-dev \
    libpq-dev \
    nmap \
    bash

ADD pyproject.toml /app/

RUN pip install --upgrade pip 
RUN pip install poetry 
RUN poetry config virtualenvs.create false 
RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app/
RUN ls -la /app
COPY entrypoint.sh /entrypoint.sh
COPY wait-for-it.sh /wait-for-it.sh

RUN chmod +x /entrypoint.sh /wait-for-it.sh


