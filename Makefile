install_all: install install_dev

install:
	pip install -U pip
	pip install -r requirements.txt

install_dev:
	pip install -U pip
	pip install -r requirements-dev.txt
	pre-commit install

test:
	pytest . -v -n auto

test_debug:
	pytest --lf -vvv --log-level=DEBUG

lint:
	pre-commit run --all-files

format:
	pre-commit run --all-files black
	pre-commit run --all-files isort

flake8:
	pre-commit run --all-files flake8

pylint:
	pre-commit run --all-files pylint

mypy:
	pre-commit run --all-files mypy
