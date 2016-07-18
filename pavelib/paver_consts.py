import os
from path import Path as path


# Constants for e2e tests
E2E_TEST_REPORT = 'e2e_tests_results.xml'
LOG_DIR = path(os.path.join('logs')).abspath()
TEST_DIR = path(os.path.join('regression', 'tests')).abspath()
REPORT_DIR = path(os.path.join('reports')).abspath()
SCREENSHOT_DIR = path(os.path.join('screenshots')).abspath()
BASELINE_DIR = path(os.path.join('certs', 'screenshots', 'baseline')).abspath()
UPLOAD_FILE_DIR = path(os.path.join('upload_files')).abspath()

# Constants for paver test in pavelib/paver_tests
PAVER_TEST_LOG_DIR = path(os.path.join('logs', 'paver_tests')).abspath()
PAVER_TEST_DIR = path(os.path.join('pavelib', 'paver_tests')).abspath()
PAVER_TEST_REPORT_DIR = path(os.path.join('reports', 'paver_tests')).abspath()
PAVER_TEST_REPORT = 'paver_tests_results.xml'
