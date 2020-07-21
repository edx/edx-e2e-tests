"""
Enterprise Course Enrollment page
"""
from __future__ import absolute_import

from bok_choy.page_object import PageObject
from six.moves import zip


class EnterpriseCourseEnrollment(PageObject):
    """
    Enterprise Course Enrollment class
    """

    COURSE_TYPE_CSS = '.radio>input[value="{}"]'

    url = None

    def is_browser_on_page(self):
        """
        Verifies if the Course confirmation title is visible on the page
        """
        return self.q(css='.course-confirmation-title').visible

    def get_course_title(self):
        """
        Returns course title
        """
        return self.q(css='.course-title').text[0]

    def target_course_type_is_present(self, course_type):
        """
        Find if provided course type is present.

        Arguments:
            course_type (str): Course type

        Returns:
            Boolean: True if desired course type is present
        """
        return self.q(
            css=self.COURSE_TYPE_CSS.format(course_type)
        ).present

    def target_course_type_is_checked(self, course_type):
        """
        Arguments:
            course_type:
        Returns:
            True(if desired course type is checked)
        """
        return self.q(
            css=self.COURSE_TYPE_CSS.format(
                course_type
            ) + '[checked="checked"]'
        ).present

    def get_course_org(self):
        """
        Returns Course Organization name
        """
        return self.q(css='.course-org').text[0]

    def get_course_info(self):
        """
        Returns Course start date
        """
        return self.q(css='.course-info>span').text[0]

    def open_course_detail_popup(self):
        """
        Open Course Detail popup
        """
        course_details_popup = '.modal-dialog .modal-content'
        self.q(css='#view-course-details-link-0').click()
        self.wait_for_element_visibility(
            course_details_popup,
            "wait for coure detail popup"
        )

    def get_course_detail_headers(self):
        """
        Returns Course Name and Organization from detail headers
        """
        detail_header_css = '.modal-content .modal-header-wrapper .details'
        course_name = self.q(
            css=detail_header_css + ' .modal-header-text'
        ).text[0]
        course_org = self.q(
            css=detail_header_css + ' .organization>img'
        ).attrs('alt')[0]
        return course_name, course_org

    def get_course_detail_body(self):
        """
        Returns details present in detail body as a dictionary where keys are
        detail titles and values are detail text
        """
        detail_header_css = '.modal-content .modal-body>.details'
        detail_title = self.q(
            css=detail_header_css + ' .detail-title-container>.title'
        ).text
        detail_value = self.q(
            css=detail_header_css + ' .detail-value-container>.text'
        ).text
        return dict(list(zip(detail_title, detail_value)))

    def get_data_sharing_consent_warning(self):
        """
        Return warning shown on declining data sharing consent
        """
        return self.q(css=".alert.warning>strong").text[0]

    def go_to_data_consent_page(self):
        """
        Go to data sharing consent page
        """
        self.q(css=".btn-confirm").click()

    def get_course_price_details(self):
        """
        Return course original price and course discounted price
        as well as the name of the organization discount provided by
        """
        return self.q(
            css='label[for="radio0"] .price'
        ).text[0]
