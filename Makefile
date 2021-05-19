PACKAGE_NAME=easy_notifyer
PACKAGE_MODULES=./$(PACKAGE_NAME) ./tests
DOCS_DIR=docs

build:
	python3 setup.py sdist bdist_wheel

install_req:
	pip3 install setuptools wheel twine

upload:
	twine upload dist/*

clean:
	@rm -rf `find . -name __pycache__`
	@rm -rf `find . -name .hash`
	@rm -rf `find . -name .md5`  # old styling
	@rm -f `find . -type f -name '*.py[co]' `
	@rm -f `find . -type f -name '*~' `
	@rm -f `find . -type f -name '.*~' `
	@rm -f `find . -type f -name '@*' `
	@rm -f `find . -type f -name '#*#' `
	@rm -f `find . -type f -name '*.orig' `
	@rm -f `find . -type f -name '*.rej' `
	@rm -f `find . -type f -name '*.md5' `  # old styling
	@rm -f .coverage
	@rm -rf htmlcov
	@rm -rf build
	@rm -rf *.egg-info
	@rm -rf cover
	@rm -rf .pytest_cache
	@rm -rf .tox
	@rm -f .develop
	@rm -f .flake
	@rm -f .install-deps
	@rm -f .install-cython

all:
	pip3 install setuptools wheel twine --upgrade && python3 setup.py sdist bdist_wheel && twine upload dist/*

pylint:
	pylint $(PACKAGE_MODULES)

flake8:
	flake8 $(PACKAGE_MODULES)

isort:
	isort $(PACKAGE_MODULES)

test:
	pytest tests/

sphinx_rst:
	sphinx-apidoc -f -o ./$(DOCS_DIR)/source $(PACKAGE_NAME)

clear_docs:
	@make --directory=./$(DOCS_DIR)/ clear

docs: clear_docs
	make --directory=./$(DOCS_DIR)/ html
