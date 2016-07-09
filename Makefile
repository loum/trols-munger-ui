PY=/usr/bin/python
NOSE=/usr/bin/nosetests -s -v --with-xunit --with-coverage --cover-erase --cover-package trols_munger_ui
NOSE_ENV=.env/bin/nosetests -s -v --with-xunit --with-coverage --cover-erase --cover-package trols_munger_ui
PYTEST=$(shell which py.test)
GIT=/usr/bin/git
COVERAGE=/usr/bin/coverage
COVERAGE_ENV=.env/bin/coverage
PYTHONPATH=.:../logga:../configa:../filer:../trols-stats

# The TESTS variable can be set to allow you to control which tests
# to run.  For example, if the current project has a test set defined at
# "tests/test_<name>.py", to run the "Test<class_name>" class:
#
# $ make test TESTS=tests:Test<class_name>
#
# To run individual test cases within each test class:
#
# $ make test TESTS=tests:Test<class_name>.test_<test_name>
#
# Note: for this to work you will need to import the test class into
# the current namespace via "tests/__init__.py"
TESTS=trols_munger_ui/tests/test_health.py::TestHealth \
	trols_munger_ui/tests/test_google.py::TestGoogle \
	trols_munger_ui/tests/test_last_update.py::TestLastUpdate \
	trols_munger_ui/tests/test_munger.py::TestMunger \
	trols_munger_ui/tests/test_players.py::TestPlayers \
	trols_munger_ui/tests/test_sections.py::TestSections \
	trols_munger_ui/tests/test_stats.py::TestStats \
	trols_munger_ui/tests/test_teams.py::TestTeams \
	trols_munger_ui/tests/test_utils.py::TestUtils

sdist:
	$(PY) setup.py sdist

rpm:
	$(PY) setup.py bdist_rpm --fix-python

docs:
	PYTHONPATH=$(PYTHONPATH) sphinx-1.0-build -b html doc/source doc/build

build: rpm

tests:
	 PYTHONPATH=$(PYTHONPATH) TROLSUI_CONF="test_config.py" \
		$(PYTEST) --capture=no -v $(TESTS)

coverage: test
	$(COVERAGE) xml -i

coverage_env: test_env
	$(COVERAGE_ENV) xml -i

uninstall:
	$(RPM) -e python-trols-munger-ui

install:
	$(RPM) -ivh dist/python-trols-munger-ui-?.?.?-?.noarch.rpm

upgrade:
	$(RPM) -Uvh dist/python-trols-munger-ui-?.?.?-?.noarch.rpm

clean:
	$(GIT) clean -xdf

.PHONY: docs rpm test
