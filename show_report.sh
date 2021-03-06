#!/bin/bash

set -e
PACKAGE_NAME=residuated_binars
pycodestyle --max-doc-length 160 --ignore E203,E501,W503 \
	    ${PACKAGE_NAME}
pylint --rcfile=.pylintrc ${PACKAGE_NAME}
mypy --config-file mypy.ini ${PACKAGE_NAME}
pytest --cov ${PACKAGE_NAME} --cov-report term-missing --cov-fail-under=50 \
       --junit-xml test-results/residuated_binars.xml \
       --doctest-modules ${PACKAGE_NAME} tests
cloc --include-lang Python ${PACKAGE_NAME}
