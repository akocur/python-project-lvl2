install:
	poetry install
test:
	poetry run pytest -vv
test-coverage:
	poetry run pytest --cov=gendiff --cov-report xml
lint:
	poetry run flake8 gendiff
selfcheck:
	poetry check
check: selfcheck test lint

build: check
	poetry build

rec:
	poetry run asciinema rec

.PHONY: install test lint selfcheck check build