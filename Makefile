install:
	pip3 install -U poetry
	poetry install

black:
	poetry run pip install black

style:
	poetry run isort -rc --atomic .
	poetry run black .
	poetry run flake8

type:
	poetry run mypy --ignore-missing-imports tests latex2mathml

check:
	poetry run safety check
	poetry run bandit -r latex2mathml

test:
	poetry run pytest --cov=latex2mathml --cov-report=xml -vv
