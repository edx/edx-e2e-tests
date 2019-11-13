from datetime import datetime

class Logger():

    def __init__(self, *args, **kwargs):
        super(Logger, self).__init__(*args, **kwargs)

    def get_tyme(self):
        '''Add date and time to console'''
        return datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")

    def do_test_name(self, name):
        '''Add tests name to console'''
        print()
        print('--- Test name is "' + name + '" ---')
        print()

    def do_click(self, name):
        '''Add text for clicking some element'''
        print('[' + self.get_tyme() + '][Click]Click on button ' + name)

    def do_input(self, name):
        '''Add text for inputing some data to some field'''
        print('[' + self.get_tyme() + '][Input]Input value in field ' + name)

    def do_text(self, name):
        '''Add some text'''
        print('[' + self.get_tyme() + '][Text]' + name)

    def test_done(self):
        '''Add text for test done'''
        print('[' + self.get_tyme() + '][Result]Test done')
