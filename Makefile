install:
	pip3 install -U poetry
	poetry install

optional:
	poetry run pip install mypy

style:
	poetry run autoflake --remove-all-unused-imports --in-place -r --exclude __init__.py .
	poetry run isort --atomic .
	poetry run black --exclude setup.py .
	poetry run flake8 .

type:
	poetry run mypy --ignore-missing-imports tests latex2mathml

check:
	poetry run safety check
	poetry run bandit -r latex2mathml

test:
	poetry run pytest --cov=latex2mathml --cov-report=xml  --cov-report=html -vv

setup:
	poetry run dephell deps convert
