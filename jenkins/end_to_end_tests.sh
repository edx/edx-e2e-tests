#!/usr/bin/env bash

# Run end-to-end tests for edx-e2e-tests in Jenkins

set -e
set -x

# Clean up the repo
# We ignore repos that we've cloned to install page objects (in .gitignore)
# so that we don't have to download them again.
git clean -xfd

# Create the virtualenv and install requirements
mkdir -p venv
virtualenv venv
. venv/bin/activate

pip install -r requirements/base.txt

# Install pages.
paver install_pages
# Run the tests
paver e2e_test
