SHELL := /bin/bash
VERBOSITY := 1

help:
	@echo "usage:"
	@echo "	make release -- release to pypi"

release:
	python setup.py register sdist bdist_wheel upload

test:
	@coverage run videos/tests/run.py --verbosity=${VERBOSITY}
	@coverage report -m
