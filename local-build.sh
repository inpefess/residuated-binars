#!/bin/bash

set -e
cd doc
make clean html
cd ..
PACKAGE_NAME=residuated_binars
pycodestyle --max-doc-length 1000 --ignore E203,E501,W503 \
	    ${PACKAGE_NAME}
pylint --rcfile=.pylintrc ${PACKAGE_NAME}
mypy --config-file mypy.ini ${PACKAGE_NAME}
pytest --cov ${PACKAGE_NAME} --cov-report term-missing --cov-fail-under=98 \
       --junit-xml test-results/residuated_binars.xml \
       --doctest-modules ${PACKAGE_NAME} tests
scc -i py ${PACKAGE_NAME}