import requests
from base64 import encodestring
from json import dumps


class SauceRestApi(object):
    """
    Class with helper methods for using the Sauce Labs RESTful API.
    See: https://saucelabs.com/docs/rest
    """
    def __init__(self, user, key):
        self.user = user
        self.key = key


    def make_url(self, suffix):
        """
        Compose the URL for the request.
        """
        url = 'https://saucelabs.com/rest/v1/{}/{}'.format(self.user, suffix)
        return url


    def update_job(self, job_id, attributes):
        """
        Update the Sauce Job

        Parameters
        ----------
        job_id: the Sauce Labs job id
        attributes: the attributes in dict format, e.g. {'passed': True}
        """
        url = self.make_url('jobs/{}'.format(job_id))
        data = dumps(attributes)
        return self.do_put(url, self.user, self.key, data)


    def do_get(self, url, user, key):
        """
        Perform a get request against the Sauce API
        """
        base64string = encodestring('{}:{}'.format(user, key))[:-1]
        headers = {'Authorization': 'Basic {}'.format(base64string),
            'Content-Type': 'application/json'}
        result = requests.get(url, headers=headers)
        assert result.status_code == 200
        return result


    def do_put(self, url, user, key, data):
        """
        Perform a put request against the Sauce API
        Note that data should be in json format.
        """
        base64string = encodestring('{}:{}'.format(user, key))[:-1]
        headers = {'Authorization': 'Basic {}'.format(base64string),
            'Content-Type': 'application/json'}

        result = requests.put(url, data=data, headers=headers)
        assert result.status_code == 200
        return result


class ParseSauceUrl(object):
    """
    Class to parse the SELENIUM_DRIVER URL to retrieve its component values.
    Example URL: sauce-ondemand:?os=Linux&browser=chrome&browser-version=28&username=foo&access-key=bar
    """
    def __init__(self, url):
        self.url = url

        self.fields = {}
        fields = self.url.split(':')[1][1:].split('&')
        for field in fields:
            [key, value] = field.split('=')
            self.fields[key] = value

    def get_value(self, key):
        """
        Get the value for the key, if it exists.
        """
        if key in self.fields:
            return self.fields[key]
        else:
            return ""
