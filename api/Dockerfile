FROM python:3.11-slim as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /api

COPY ./api/poetry.lock ./api/pyproject.toml ./

RUN pip install "poetry" \
    && poetry install --no-root --no-ansi --no-interaction \
    && poetry export -f requirements.txt -o requirements.txt --without development

FROM python:3.11-slim as final

WORKDIR /api

COPY --from=builder /api/requirements.txt .

RUN set -ex \
    && addgroup --system --gid 1001 appgroup \
    && adduser --system --uid 1001 --gid 1001 --no-create-home appuser \
    && apt-get update \
    && apt-get upgrade -y \
    && pip install -r requirements.txt \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./api/alembic alembic
COPY ./api/alembic.ini ./
COPY ./api api
COPY ./api/my_locations_api my_locations_api
