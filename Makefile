################################################################################
# Makefile for BWPlanner.
################################################################################
.PHONY: all lint test

all: lint test

lint:
	@pylint -v bwplanner.py domain/ solvers/

test:
	@pytest --cov=. --cov-report=xml --cov-report=term-missing tests/
