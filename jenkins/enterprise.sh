#!/usr/bin/env bash

# Run end-to-end tests for edx-e2e-tests in Jenkins

set -e
set -x

# Clean up the repo
# We ignore repos that we've cloned to install page objects (in .gitignore)
# so that we don't have to download them again.
git clean -xfd > log/git_clean.log

# Create the virtualenv and install requirements
mkdir -p venv
python -m virtualenv --python=python3.5 venv
. venv/bin/activate

echo "Installing base requirements"
mkdir -p log
pip install -r requirements/base.txt > log/pip_install_base.log

# Set the display to the virtual frame buffer (Xvfb)
export DISPLAY=:1

# Run the tests
paver enterprise
