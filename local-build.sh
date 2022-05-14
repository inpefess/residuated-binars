#!/bin/bash

set -e
cd doc
make clean html
cd ..
PACKAGE_NAME=residuated_binars
flake8 ${PACKAGE_NAME}
pylint ${PACKAGE_NAME}
mypy ${PACKAGE_NAME}
pytest --cov-report term-missing ${PACKAGE_NAME} tests
scc -i py ${PACKAGE_NAME}
