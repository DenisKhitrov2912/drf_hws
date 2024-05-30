FROM python:latest

WORKDIR /app

COPY pyproject.toml /

COPY poetry.lock /

RUN poetry install --no-dev

COPY . .