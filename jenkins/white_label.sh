#!/usr/bin/env bash

# Run end-to-end tests for edx-e2e-tests in Jenkins

set -e
set -x

cd edx-e2e-tests

# Clean up previous builds
git clean -qxfd

export DISPLAY=":1"

python -m virtualenv --python=python3.8 venv
. venv/bin/activate

mkdir -p log

pip install -r requirements/base.txt

# Run the tests
organizations=""

for organization in ${organizations}; do
    export SELENIUM_BROWSER=chrome
    export ORG=${organization}
    echo "Running wl tests on" ${organization}
    paver e2e_wl_test || EXIT=1
done


exit ${EXIT}
