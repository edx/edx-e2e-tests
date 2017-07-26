"""
End-to-end test cases
"""

import os

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

if not os.environ.get('SELENIUM_HOST', '').startswith('edx.devstack'):
    # Hack until we switch to Chrome or upgrade Firefox in Jenkins
    DesiredCapabilities.FIREFOX['marionette'] = False
