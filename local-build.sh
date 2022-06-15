#!/bin/bash

set -e
cd doc
make clean html
cd ..
PACKAGE_NAME=residuated_binars
pydocstyle ${PACKAGE_NAME} tests
flake8 ${PACKAGE_NAME} tests
pylint ${PACKAGE_NAME} tests
mypy ${PACKAGE_NAME} tests
pytest --cov-report term-missing ${PACKAGE_NAME} tests
scc -i py ${PACKAGE_NAME}
