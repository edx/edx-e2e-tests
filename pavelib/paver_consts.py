from path import Path as path

# Paths for different directories
LOG_DIR = path('./logs').abspath()
TEST_DIR = path('./stage/tests/').abspath()
REPORT_DIR = path('./reports').abspath()
SCREENSHOT_DIR = path('./screenshots').abspath()
BASELINE_DIR = path('./certs/screenshots/baseline').abspath()

# XML reports names
SMOKE_TEST_REPORT = '/smoke_tests_results.xml'
