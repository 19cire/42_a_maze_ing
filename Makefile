PYTHON	= .venv/bin/python3
PIP		= .venv/bin/pip
SRC		= a_maze_ing.py
CONFIG	= config.txt
VENV	= .venv

$(VENV):
	python3 -m venv $(VENV)

install: $(VENV)
	$(PIP) install pytest flake8 mypy

all: run

run:
	python3 a_maze_ing.py config.txt $(ARGS)

test: 
	@echo "Running test..."
	$(PYTHON) -m pytest

debug:
	$(PYTHON) -m pdb $(SRC)

lint:
	flake8 $(SRC)
	mypy $(SRC) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 *.py
	mypy --strict *.py

clean:
	rm -rf .mypy_cache .pytest_cache

.PHONY: all run test debug lint lint-strict clean