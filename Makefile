.PHONY: install
install:
	pip3 install -U pip setuptools poetry
	poetry install

.PHONY: install-no-venv
install-no-venv:
	pip3 install -U pip setuptools poetry
	poetry config virtualenvs.create false
	poetry install

.PHONY: style
style:
	poetry run autoflake --remove-all-unused-imports --in-place -r --exclude __init__.py .
	poetry run isort .
	poetry run black .

.PHONY: format
format: style

.PHONY: lint
lint:
	poetry run autoflake --remove-all-unused-imports --in-place -r --exclude __init__.py --check .
	poetry run isort --check-only .
	poetry run black --check .
	poetry run flake8 .
	poetry run mypy tests latex2mathml

.PHONY: test
test:
	poetry run pytest --cov=latex2mathml --cov-report=xml --cov-report=html -vv

.PHONY: setup
setup:
	poetry run dephell deps convert
