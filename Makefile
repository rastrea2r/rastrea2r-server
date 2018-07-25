# This makefile has been created to help developers perform common actions.
# Most actions assume it is operating in a virtual environment where the
# python command links to the appropriate virtual environment Python.

VENVS_DIR := ./.venv
VENV_DIR := $(VENVS_DIR)/rastrea2r_server

# Do not remove this block. It is used by the 'help' rule when
# constructing the help output.
# help:
# help: rastrea2r_server Makefile help
# help:

# help: help                           - display this makefile's help information
.PHONY: help
help:
	@grep "^# help\:" Makefile | grep -v grep | sed 's/\# help\: //' | sed 's/\# help\://'

# help: venv                           - create a virtual environment for development
.PHONY: venv
venv:
	@test -d "$(VENVS_DIR)" || mkdir -p "$(VENVS_DIR)"
	@rm -Rf "$(VENV_DIR)"
	@python3 -m venv "$(VENV_DIR)"
	@/bin/bash -c "source $(VENV_DIR)/bin/activate && pip install pip --upgrade && pip install -r requirements.dev.txt && pip install -e ."
	@echo "Enter virtual environment using:\n\n\t$ source $(VENV_DIR)/bin/activate\n"


# help: clean                          - clean all files using .gitignore rules
.PHONY: clean
clean:
	@git clean -X -f -d


# help: scrub                          - clean all files, even untracked files
.PHONY: scrub
scrub:
	git clean -x -f -d


# help: test                           - run tests
.PHONY: test
test:
	@python -m unittest discover -s tests


# help: test-verbose                   - run tests [verbosely]
.PHONY: test-verbose
test-verbose:
	@python -m unittest discover -s tests -v


# help: check-coverage                 - perform test coverage checks
.PHONY: check-coverage
check-coverage:
	@coverage run -m unittest discover -s tests
	@# produce html coverage report on modules
	@coverage html -d docs/source/coverage --include="src/rastrea2r_server/*"
	@# rename coverage html file for latter use with documentation
	@cd docs/source/coverage; mv index.html coverage.html


# help: style                          - perform code format compliance check
.PHONY: style
style:
	@black src/rastrea2r_server tests



# help: check-types                    - check type hint annotations
.PHONY: check-types
check-types:
	@cd src; MYPYPATH=$(VENV_DIR)/lib/python*/site-packages mypy -p rastrea2r_server --ignore-missing-imports


# help: docs                           - generate project documentation
.PHONY: check-coverage
docs: check-coverage
	@cd docs; rm -rf source/api/rastrea2r_server*.rst source/api/modules.rst build/*
	@cd docs; make html
	@# Copy coverage output into docs build tree
	@cd docs; cp -R source/coverage build/html/.


# help: check-docs                     - quick check docs consistency
.PHONY: check-docs
check-docs:
	@cd docs; make dummy


# help: serve-docs                     - serve project html documentation
.PHONY: serve-docs
serve-docs:
	@cd docs/build; python -m http.server --bind 127.0.0.1


# Keep these lines at the end of the file to retain nice help
# output formatting.
# help:
