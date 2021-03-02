################################################################################
# Makefile for BWPlanner.
################################################################################
.PHONY: all test

all: test

test:
	@pylint -v bwplanner.py domain/ solvers/
	@pytest --cov-report=xml --cov=. tests/
