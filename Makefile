TEMP_CHANGES = changes.tmp.md
SOURCES = flask_api_builder.py
COV_ARGS = --source=$(SOURCES) --branch
PYTEST_ARGS = 
TESTS = tests.py
BROWSER = chromium-browser

coverage:
	coverage run $(COV_ARGS) -m pytest $(PYTEST_ARGS) $(TESTS)
	coverage html
	coverage report
	@echo 
	$(RM) .coverage
	$(BROWSER) htmlcov/index.html

tests:
	py.test $(TESTS)

changes:
	auto-changelog -o $(TEMP_CHANGES)
	pandoc --from=markdown --to=rst -o CHANGELOG.rst $(TEMP_CHANGES)
	$(RM) $(TEMP_CHANGES)

.PHONY: changes coverage tests
