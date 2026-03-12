.PHONY: install
install:
	uv sync

.PHONY: format
format:
	uv run ruff check --fix .
	uv run ruff format .

.PHONY: lint
lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy tests latex2mathml

.PHONY: test
test:
	uv run pytest

.PHONY: tag
tag:
	VERSION=`uv run python -c "import importlib.metadata; print(importlib.metadata.version('latex2mathml'))"`; \
	git tag -s -a $$VERSION -m "Release $$VERSION"; \
	echo "Tagged $$VERSION";
