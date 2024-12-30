#!/usr/bin/env bash

set -e

COVERAGE_DIR="src/ally_security/assistant/*"

if [[ -z "${PYLOG_HOME}" ]]; then
    if [[ -f find_home.sh ]]; then
        source find_home.sh
    else
        source bin/find_home.sh
    fi
fi

source "${PYLOG_HOME}/bin/setup_venv.sh"

PYTHONPATH="${VENV_HOME}/bin"
PYTHONPATH="${PYTHONPATH}:${PYLOG_HOME}/src" coverage run --rcfile="${PYLOG_HOME}/.coveragerc" -m pytest -v "${PYLOG_HOME}/src/test"

coverage report -m

coverage html --include "${COVERAGE_DIR}"
