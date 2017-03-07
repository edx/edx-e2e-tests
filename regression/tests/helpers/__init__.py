from bok_choy.web_app_test import WebAppTest
from castroredux import CastroRedux

class BaseTestClass(WebAppTest):
    """ Base class for all tests in studio """
    def setUp(self):
        super(BaseTestClass, self).setUp()

        # write the vnc password to a file, because that is the
        # easiest way to get it over to the capture tool
        # without user interaction.
        VNC_PASSWORD_FILE = '/tmp/pass.txt'
        with open(VNC_PASSWORD_FILE, 'w') as pass_file:
            pass_file.write('secret')

        self.castro = CastroRedux(
            'screenshots/{}.flv'.format(self.id()),
            host = '10.0.2.2',
            port = 5900,
            pwdfile = VNC_PASSWORD_FILE
        )

        self.castro.start()
        self.addCleanup(self.castro.stop)