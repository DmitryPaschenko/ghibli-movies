tests = tests
package = movies

check:
	# No unused imports, no undefined vars,
	flake8 --ignore=E704,E731,W503,W504,R1710 --exclude $(package)/__init__.py,$(package)/compat.py,$(package)/db_config/* --max-line-length=100 --max-complexity 10 $(package)/
	flake8 --ignore=E731,W503,F401,W504,R1710 --max-complexity 10 $(package)/compat.py
	# Basic error checking in test code
	pyflakes $(tests)
	# Python linter errors only
	pylint --rcfile .pylintrc $(package)

pylint:
	pylint --rcfile .pylintrc $(package)

test:
	python -m pytest -v $(tests)
