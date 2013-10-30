#!/usr/bin/env bash

set -x

# Edit the "jenkins_env" file to set your
# credentials and desired browser
source jenkins_env

# Start SauceConnect running locally
java -jar /usr/local/bin/Sauce-Connect.jar $SAUCE_USER_NAME $SAUCE_API_KEY -P $SELENIUM_PORT
