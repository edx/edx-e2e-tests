import os
from .sauce_helpers import ParseSauceUrl
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BrowserEnv(object):
    """
    Class to hold the browser environment settings.
    These are determined by OS environment values.
    """
    def __init__(self):

        # Take a local copy of the OS environment because we do
        # not need to change the values for this shell
        # Note that if you are running on Jenkins with the SauceLabs
        # plug-in, the values of these environment variables will
        # be set for you by the build.
        osenv = os.environ.copy()

        # If you want to run on a Selenium Grid (e.g. a local one, or at
        # SauceLabs) then set up these environment variables.
        # If you want to run a local browser, you do not need to set these.

        # Example values for a local selenium grid:
        # os.environ['SELENIUM_HOST'] = 'localhost'
        # os.environ['SELENIUM_PORT'] = '4444'

        # Example values for Sauce Labs:
        # os.environ['SELENIUM_HOST'] = 'ondemand.saucelabs.com'
        # os.environ['SELENIUM_PORT'] = '80'
        self.selenium_host = osenv.get('SELENIUM_HOST')
        self.selenium_port = osenv.get('SELENIUM_PORT')

        # Browser to use, default to Google Chrome.
        # This value is also used as the browser choice
        # when running a local webdriver.
        self.selenium_browser = osenv.get('SELENIUM_BROWSER', 'chrome')

        # Platform and Version choices to pass to the selenium grid.
        # If you are running a local browser, or if you do not care to
        # specify the OS and browser version, then you do not need to set them.
        self.selenium_platform = osenv.get('SELENIUM_PLATFORM')
        self.selenium_version = osenv.get('SELENIUM_VERSION')

        # The SauceLabs credentials to use.
        # Again, if you are running from a Jenkins job, they will be
        # set for you by the plug-in. In a multi-configuration job,
        # the browser specs are populated into the SELENIUM_DRIVER
        # variable and we will parse them out from there.
        self.selenium_driver = osenv.get('SELENIUM_DRIVER')
        self.sauce_user_name = osenv.get('SAUCE_USER_NAME')
        self.sauce_api_key = osenv.get('SAUCE_API_KEY')
        self.run_on_saucelabs = bool(
            self.selenium_host == 'ondemand.saucelabs.com'
            or self.selenium_driver
            )

        # BUILD_NUMBER and JOB_NAME get set by Jenkins itself.
        # Not needed for local browser, private grid, or local SauceConnect.
        self.run_on_jenkins = bool(osenv.get('JOB_NAME'))
        self.build_number = osenv.get('BUILD_NUMBER', 'local harvest')
        self.job_name = osenv.get('JOB_NAME', 'acceptance tests')

        # This will be filled in later once the webdriver starts up.
        # It is needed to communicate with SauceLabs to update the
        # job, for example with the pass/fail status.
        self.session_id = None

        # When run as a multi-configuration project on Jenkins the
        # SELENIUM_DRIVER url will be populated and its values
        # need to be extracted and used instead of the individual
        # os environment values.
        # example url: sauce-ondemand:?os=Linux&browser=chrome&browser-version=28&username=foo&access-key=bar
        if self.selenium_driver:
            parse = ParseSauceUrl(self.selenium_driver)
            self.sauce_user_name = parse.get_value('username')
            self.sauce_api_key = parse.get_value('access-key')
            self.selenium_browser = parse.get_value('browser')
            self.selenium_version = parse.get_value('browser-version')
            sauce_driver_os = parse.get_value('os')
            if 'Windows 2003' in sauce_driver_os:
                self.selenium_platform = 'XP'
            elif 'Windows 2008' in sauce_driver_os:
                self.selenium_platform = 'VISTA'
            elif 'Linux' in sauce_driver_os:
                self.selenium_platform = 'LINUX'
            else:
                self.selenium_platform = sauce_driver_os


    def _make_desired_capabilities(self):
        """
        Compose and return a DesiredCapabilities object with the
        browser attributes that you want.
        """
        # Figure out the starting desired capablilities from the browser choice.
        # Note that this pulls in the defaults for browserName,
        # version, platform, and javascriptEnabled from selenium.
        desired_capabilities = {}
        if self.selenium_browser == 'android':
            desired_capabilities = DesiredCapabilities.ANDROID
        elif self.selenium_browser == 'chrome':
            desired_capabilities = DesiredCapabilities.CHROME
        elif self.selenium_browser == 'firefox':
            desired_capabilities = DesiredCapabilities.FIREFOX
        elif self.selenium_browser == 'htmlunit':
            desired_capabilities = DesiredCapabilities.HTMLUNIT
        elif self.selenium_browser == 'iexplore':
            desired_capabilities = DesiredCapabilities.INTERNETEXPLORER
        elif self.selenium_browser == 'iphone':
            desired_capabilities = DesiredCapabilities.IPHONE
        else:
            desired_capabilities = DesiredCapabilities.FIREFOX

        if self.selenium_version:
            desired_capabilities['version'] = self.selenium_version
        if self.selenium_platform:
            desired_capabilities['platform'] = self.selenium_platform

        if self.run_on_saucelabs:
            desired_capabilities['video-upload-on-pass'] = False
            desired_capabilities['sauce-advisor'] = False
            desired_capabilities['capture-html'] = True
            desired_capabilities['record-screenshots'] = True
            desired_capabilities['max-duration'] = 600
            desired_capabilities['public'] = 'public restricted'
            desired_capabilities['build'] = self.build_number
            desired_capabilities['name'] = self.job_name

        return desired_capabilities
