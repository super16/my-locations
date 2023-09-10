# my-location API

Requires [poetry](https://python-poetry.org/).

```shell
poetry install
```

## Lint

```shell
poetry run flake8
poetry run mypy .
poetry run ruff . --fix 
```

## Test

Check that `locations_db` container is launched to run tests. 

```shell
poetry run pytest
```
