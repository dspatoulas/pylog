#!/usr/bin/env bash

set -e

if [[ -z "${PYLOG_HOME}" ]]; then

    echo "Trying to locate PYLOG_HOME"

    while [[ ${PWD} != "/" ]]; do

        echo "Checking path ${PWD}"

        if [[ -f "${PWD}/pyproject.toml" ]]; then
            PROJECT_NAME=$(yq -p toml -o json < "${PWD}/pyproject.toml" | jq -r '.tool.poetry.name')
            PYLOG_HOME="${PWD}"
            echo "Found ${PROJECT_NAME} at ${PYLOG_HOME}"
            export PYLOG_HOME
            break
        else
            echo "Unable to find home in this directory, moving one directory up"
            pushd ../
        fi

    done

    if [[ -z "${PYLOG_HOME}" ]]; then
        echo "Unable to locate PYLOG_HOME"
        exit 1
    fi

else
    echo "PYLOG_HOME already set to ${PYLOG_HOME}"
fi
