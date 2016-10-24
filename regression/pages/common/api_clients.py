"""
API classes for different tasks
"""
import requests
from requests.auth import AuthBase
from edx_rest_api_client.client import EdxRestApiClient

from regression.pages.whitelabel.const import (
    ACCESS_TOKEN,
    AUTH_PASSWORD,
    AUTH_USERNAME,
    ECOMMERCE_API_URL,
    ENROLLMENT_API_URL,
    URL_WITHOUT_AUTH
)


class ApiException(Exception):
    """
    Exceptions for API failures
    """
    pass


def check_response(response):
    """
    Check whether a response was successful. If not raise an exception
    Args:
        response:
    """
    if response.status_code != 200:
        raise ApiException(
            'API request failed with following error code: ' +
            str(response.status_code)
        )


class BearerAuth(AuthBase):
    """ Attaches Bearer Authentication to the given Request object. """

    def __init__(self, token):
        """ Instantiate the auth class. """
        self.token = token

    def __call__(self, r):
        """ Update the request headers. """
        r.headers['Authorization'] = 'Bearer {}'.format(self.token)
        return r


class EcommerceApiClient(object):
    """
    Ecommerce API client for various actions like creating, deleting
    downloading coupons
    """

    @property
    def ecommerce_api_client(self):
        """
        E-Commerce API Client
        """
        return EdxRestApiClient(
            ECOMMERCE_API_URL, oauth_access_token=ACCESS_TOKEN)

    def create_coupon(self, payload):
        """
        Create coupons using API
        Args:
            payload:
        """
        response = self.ecommerce_api_client.coupons.post(data=payload)
        check_response(response)
        return response['coupon_id']

    def get_coupon_report(self, coupon_id):
        """
        Get coupon report using api
        Args:
            coupon_id:
        """
        response = self.ecommerce_api_client.products(coupon_id).get()
        check_response(response)
        return response

    def delete_coupon(self, coupon_id):
        """
        Delete the coupon created in the tests and all associated stock
        records and vouchers.
        Args:
            coupon_id:
        """
        response = self.ecommerce_api_client.coupons(coupon_id).delete()
        check_response(response)

    def get_coupon_codes(self, coupon_id):
        """
        Get coupon codes from coupon report
        Args:
            coupon_id:
        """
        coupon_codes = []
        items = (
            self.get_coupon_report(coupon_id)['attribute_values'][0]['value']
        )
        check_response(items)
        for item in items:
            coupon_codes.append(item['code'])
        return coupon_codes


class EnrollmentApiClient(object):
    """
    Enrollment API client
    """

    def __init__(self, host=None, key=None):
        self.host = host or ENROLLMENT_API_URL
        self.key = key or ACCESS_TOKEN

    def is_use_enrolled_in_the_course(self, username, course_id):
        """
        Retrieve the enrollment status for given user in a given course.
        Args:
            username:
            course_id:
        Returns:
            True or false based on whether user is enrolled
        """
        url = '{host}/enrollment/{username},{course_id}'.format(
            host=self.host,
            username=username,
            course_id=course_id
        )
        response = requests.get(url, auth=BearerAuth(self.key))
        check_response(response)
        formatted_response = response.json()
        return formatted_response['is_active']


class LmsApiClient(object):
    """
    API class for accessing different APIs
    """

    def __init__(self, host=None):
        """
        Instantiate the api class.
        """
        self.host = host or URL_WITHOUT_AUTH
        self.session = requests.Session()
        self.session.auth = (AUTH_USERNAME, AUTH_PASSWORD)

    def _post_headers(self, x_csrf=None):
        """
        Default HTTP headers dict.
        Args:
            x_csrf:
        """
        return {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.host,
            'X-CSRFToken': x_csrf,
        }

    def get_target_site_session(self):
        """
        Open target site using requests and return cookies
        Returns:
            cookies
        """
        response = self.session.get(self.host)
        check_response(response)
        self.session.cookies = response.cookies
        self.session.headers = self._post_headers(
            response.cookies['csrftoken']
        )

    def get_login_session(self, user_email, user_password):
        """
        Create a session and assign cookies to it after successful login
        Args:
            user_email:
            user_password:
        """
        self.get_target_site_session()
        login_url = self.host + 'user_api/v1/account/login_session/'
        payload = {
            'email': user_email,
            'password': user_password,
            'remember': 'false'
        }
        response = self.session.post(login_url, data=payload)
        check_response(response)
        self.session.cookies = response.cookies
        self.session.headers = self._post_headers(
            response.cookies['csrftoken']
        )

    def change_enrollment(self, course_id, enrollment_action):
        """
        Change enrollment
        Args:
            course_id:
            enrollment_action:
        Returns:
            True if no exception is generated
        """
        change_enrollment_url = self.host + 'change_enrollment'
        payload = {
            'course_id': course_id,
            'enrollment_action': enrollment_action
        }
        response = self.session.post(
            change_enrollment_url,
            data=payload
        )
        check_response(response)
        return True

    def get_coupon_request(self, target_url):
        """
        Send a Get request and return the response if successful
        Args:
          target_url:
        """
        response = self.session.get(target_url)
        check_response(response)
        return response.content
