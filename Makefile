install:
	pip3 install -U pip poetry
	poetry install

test:
	poetry run isort -rc --atomic .
	poetry run black .
	poetry run flake8
	poetry run pytest --cov=latex2mathml --cov-report=xml -vv -x
