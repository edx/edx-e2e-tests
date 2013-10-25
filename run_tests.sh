#!/usr/bin/env bash

set -x

# Always execute paths relative to this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Execute tests
nosetests $SCRIPT_DIR/edx_tests/tests
