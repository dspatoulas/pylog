#!/usr/bin/env bash

set -e

if [[ -z "${PYLOG_HOME}" ]]; then
    if [[ -f find_home.sh ]]; then
        source find_home.sh
    else
        source bin/find_home.sh
    fi
fi

if [[ -z "${VENV_HOME}" ]]; then
  source "${PYLOG_HOME}/bin/setup_venv.sh"
else
  echo "VENV_HOME: ${VENV_HOME}"
fi

echo "Activating VENV_HOME from location ${VENV_HOME}"

source "${VENV_HOME}/bin/activate"

black "$@"
isort --profile=black "$@"
#autoflake -r --in-place --remove-unused-variables "$@"
