run:
	python3 code/main.py

precommit: all_tests format

format:

	pre-commit run --all-files

all_tests:
	pytest test/

cov:
	coverage run -m pytest test/

rep:
	clear
	coverage report -m
	coverage html

test_cov: cov rep
