FROM python:3.11

WORKDIR /api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="${PATH}:/root/.local/bin"

COPY ./my_locations_api /api/my_locations_api
COPY ./poetry.lock /api/poetry.lock
COPY ./pyproject.toml /api/pyproject.toml

RUN poetry install
