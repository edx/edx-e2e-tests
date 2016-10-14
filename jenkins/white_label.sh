#!/usr/bin/env bash

# Run end-to-end tests for edx-e2e-tests in Jenkins

set -e
set -x

# Clean up previous builds
git clean -qxfd

cd edx-e2e-tests

export DISPLAY=":1"

virtualenv venv
. venv/bin/activate

pip install -r requirements/base.txt


# Run the tests
organizations="MITProfessionalX HarvardXPLUS"

# Run General tests on all organizations using Firefox
for organization in ${organizations}; do
    export ORG=${organization}
    echo "Running General tests using Firefox on" ${organization}
    paver e2e_wl_test general || EXIT=1
done


# Run Coupon tests on all organizations using chrome
for organization in ${organizations}; do
    export SELENIUM_BROWSER=chrome
    export ORG=${organization}
    echo "Running Coupon tests using Chrome on" ${organization}
    paver e2e_wl_test coupon || EXIT=1
done


exit ${EXIT}
