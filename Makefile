################################################################################
# Makefile for BWPlanner.
################################################################################
.PHONY: all setup lint test

VENV := .venv
# Use the virtual environment's tools if it exists, the system ones otherwise.
BIN := $(if $(wildcard $(VENV)/bin),$(VENV)/bin/,)

all: lint test

# Create a virtual environment and install the dependencies into it.
setup:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

lint:
	@$(BIN)pylint -v bwplanner.py domain/ solvers/

test:
	@$(BIN)pytest --cov=. --cov-report=xml --cov-report=term-missing tests/
