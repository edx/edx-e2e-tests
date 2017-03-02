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

# Install the page objects from the edx-platform repo.
# Before doing so, we don't need optimizations for lxml,
# so install it this way which doesn't bother compiling them.
STATIC_DEPS=true CFLAGS="-O0"  pip install "lxml==3.4.4"
paver install_pages

# Set the display to the virtual frame buffer (Xvfb)
export DISPLAY=:1

# Run the tests
paver e2e_test --with-flaky
