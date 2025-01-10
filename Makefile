.PHONY: format
format:
	@uv run ruff check src tests --fix-only
	@uv run ruff format src tests

.PHONY: format-check
format-check:
	@uv run ruff format src --check

.PHONY: mypy
mypy:
	@uv run mypy src tests

.PHONY: ruff
ruff:
	@uv run ruff check src tests

.PHONY: pytest
pytest:
	@uv run pytest
	@uv run --with-requirements requirements-min.txt python -m pytest

.PHONY: lint
lint: format-check mypy ruff

.PHONY: all
all: format mypy ruff pytest

.DEFAULT_GOAL := all
