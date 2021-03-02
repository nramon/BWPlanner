################################################################################
# Makefile for BWPlanner.
################################################################################
.PHONY: all test

all: test

test:
	@pylint -v bwplanner.py domain/ solvers/
	@py.test-3 --cov-report=xml --cov=. tests/
