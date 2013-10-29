SHELL := /bin/bash

help:
	@echo "usage:"
	@echo "	make release -- release to incuna pypi"

release:
	python setup.py register -r incuna sdist upload -r incuna
