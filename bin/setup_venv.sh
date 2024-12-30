#!/usr/bin/env bash

set -e

# Override in Container and Pipelines to target correct version for Production Spark (python3.10 or python 3.11)
DEFAULT_PYTHON_VERSION="python3.13"
PYTHON_VERSION="${PYTHON_VERSION:-$DEFAULT_PYTHON_VERSION}"

if [[ -z "${PYLOG_HOME}" ]]; then
    if [[ -f find_home.sh ]]; then
        source find_home.sh
    else
        source bin/find_home.sh
    fi
fi

VENV_HOME="${PYLOG_HOME}/venv"

echo "Setting venv location to ${VENV_HOME}"

if [[ ! -d "${VENV_HOME}" ]]; then

    echo "Venv does not exist, trying to create using ${PYTHON_VERSION}"

    virtualenv "${VENV_HOME}" --python="${PYTHON_VERSION}"

else
    echo "Venv already exists, skipping setup"
fi

export VENV_HOME

source "${VENV_HOME}/bin/activate"

# Adjust the lockfile for new entries to the pyproject.toml
# that have been added without using `poetry add` command
# poetry lock --no-update

# Install the current project dependencies
poetry install --no-root
