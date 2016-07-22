TEMP_CHANGES = changes.tmp.md
SOURCES = flask_api_builder.py
COV_ARGS = --source=$(SOURCES) --branch
PYTEST_ARGS = 
TESTS = tests.py
BROWSER = chromium-browser
PYLINT_ARGS = --reports=no --output-format=colorized

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

sdist:
	python setup.py sdist

wheel:
	python setup.py bdist_wheel

.PHONY: changes coverage tests
