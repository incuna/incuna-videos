SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "	make release -- release to pypi"

release:
	python setup.py register sdist upload

test:
	@coverage run videos/tests/run.py
	@coverage report
