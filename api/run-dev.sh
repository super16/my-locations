#!/bin/bash

poetry run alembic upgrade head
poetry run sanic my_locations_api:api --host=0.0.0.0 --port=8000 --reload --workers=2
