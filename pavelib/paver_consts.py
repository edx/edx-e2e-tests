import os
from path import Path as path


# XML report name for smoke tests
SMOKE_TEST_REPORT = 'smoke_tests_results.xml'

LOG_DIR = path(os.path.join('logs')).abspath()
TEST_DIR = path(os.path.join('regression', 'tests')).abspath()
REPORT_DIR = path(os.path.join('reports')).abspath()
SCREENSHOT_DIR = path(os.path.join('screenshots')).abspath()
BASELINE_DIR = path(os.path.join('certs', 'screenshots', 'baseline')).abspath()