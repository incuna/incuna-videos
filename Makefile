SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "	make release -- release to incuna pypi"

release:
	python setup.py register -r incuna sdist upload -r incuna

test:
	@coverage run videos/tests/run.py
	@coverage report
