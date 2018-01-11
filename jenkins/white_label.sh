#!/usr/bin/env bash

# Run end-to-end tests for edx-e2e-tests in Jenkins

set -e
set -x

cd edx-e2e-tests

# Clean up previous builds
git clean -qxfd

export DISPLAY=":1"

virtualenv venv
. venv/bin/activate

mkdir -p log

pip install -r requirements/base.txt

# Install the page objects from the edx-platform repo.
# Before doing so, we don't need optimizations for lxml,
# so install it this way which doesn't bother compiling them.
STATIC_DEPS=true CFLAGS="-O0"  pip install "lxml==4.0.0" > log/pip_lxml_install.log
paver install_pages > log/paver_install_pages.log


# Run the tests
organizations="MITxPRO HarvardMedGlobalAcademy"

for organization in ${organizations}; do
    export ORG=${organization}
    echo "Running wl tests on" ${organization}
    paver e2e_wl_test || EXIT=1
done


exit ${EXIT}
