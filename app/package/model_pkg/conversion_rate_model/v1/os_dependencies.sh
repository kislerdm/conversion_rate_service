#! /bin/bash

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
BASE_DIR=$( dirname "${BASE_DIR}" )

exec ${BASE_DIR}/install_dependencies.sh libgomp1