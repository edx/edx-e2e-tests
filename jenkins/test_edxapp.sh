#!/usr/bin/env bash

# Run end-to-end tests for edxapp and other services in Jenkins
# Assumes that the following environment variables are set:
#
# TEST_ENV_HOST: hostname to run the tests on (e.g. test.domain.org)
#   Assumes that Studio is served from studio.$TEST_ENV_HOST
#
# BASIC_AUTH_USER and BASIC_AUTH_PASSWORD: basic auth credentials; can be blank
#
# REGISTRATION_EMAIL: email used to register for new courses (e.g. test@example.com)
#
# SSH_USER and SSH_KEYFILE: user and private key to ssh into the test server
#
# Optional: Saucelabs plugin may set additional environment variables,
# which are printed to make debugging easier

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
fab install_pages

# Debug information
echo "SELENIUM_BROWSER=$SELENIUM_BROWSER"
echo "SELENIUM_VERSION=$SELENIUM_VERSION"
echo "SELENIUM_PLATFORM=$SELENIUM_PLATFORM"

# Configure the test
fab config_lms:protocol=http
fab config_lms:test_host=$TEST_ENV_HOST
fab config_lms:basic_auth_user=$BASIC_AUTH_USER
fab config_lms:basic_auth_password=$BASIC_AUTH_PASSWORD

fab config_studio:protocol=http
fab config_studio:test_host=studio.$TEST_ENV_HOST
fab config_studio:basic_auth_user=$BASIC_AUTH_USER
fab config_studio:basic_auth_password=$BASIC_AUTH_PASSWORD

# Run the tests
fab test_lms
fab test_studio
