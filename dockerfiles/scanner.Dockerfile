FROM python:3-slim

WORKDIR /scanner

RUN python -m pip install --upgrade pip && pip install poetry
RUN apt-get update && apt-get -y install gcc

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml

RUN poetry install

COPY . .
