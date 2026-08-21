PYTHON	= $(VENV)/bin/python3
PIP		= $(VENV)/bin/pip
SRC		= a_maze_ing.py
CONFIG	= config.txt
VENV	= matrix

$(VENV):
	python3.11 -m venv $(VENV)

install: $(VENV)
	$(PIP) install pytest flake8 mypy

all: run

run:
	python3 a_maze_ing.py config.txt $(ARGS)

test: 
	@echo "Running test..."
	$(PYTHON) -m pytest mytest.py

debug:
	$(PYTHON) -m pdb $(SRC)

lint:
	flake8 $(SRC)
	mypy $(SRC)

lint-strict:
	flake8 *.py
	mypy --strict -python-version 3.11 .

clean:
	rm -rf .mypy_cache .pytest_cache

.PHONY: all run test debug lint lint-strict clean