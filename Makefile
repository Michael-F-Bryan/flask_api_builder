TEMP_CHANGES = changes.tmp.md
SOURCES = flask_api_builder.py
COV_ARGS = --source=$(SOURCES) --branch
PYTEST_ARGS = 
TESTS = tests
BROWSER = chromium-browser
PYLINT_ARGS = --reports=no --output-format=colorized
DIST_FILES = $(wildcard dist/*)
GPG_IDENTITY = michaelfbryan@gmail.com


coverage:
	coverage run $(COV_ARGS) -m pytest $(PYTEST_ARGS) $(TESTS)
	coverage html
	coverage report
	@echo 
	$(RM) .coverage
	$(BROWSER) htmlcov/index.html

tests:
	py.test $(TESTS)

lint:
	-pylint $(PYLINT_ARGS) flask_api_builder.py


changes:
	auto-changelog -o $(TEMP_CHANGES)
	pandoc --from=markdown --to=rst -o CHANGELOG.rst $(TEMP_CHANGES)
	$(RM) $(TEMP_CHANGES)


bump-patch:
	bumpversion patch

bump-minor:
	bumpversion minor

bump-major:
	bumpversion major


clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	
clean-test: ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/


sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

dist: clean sdist wheel ## builds source and wheel package
	ls -l dist
release: dist
	twine register $(DIST_FILES)
	twine upload $(DIST_FILES) --sign --identity $(GPG_IDENTITY)


.PHONY: changes coverage tests lint
.PHONY: bump-minor bump-patch bump-major 
.PHONY: sdist wheel dist release
.PHONY: clean clean-build clean-pyc clean-test
