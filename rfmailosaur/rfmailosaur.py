from mailosaur import MailosaurClient
from mailosaur.models import SearchCriteria
from robot.api.deco import keyword, library
from robot.api import logger


@library
class RFMailosaur:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.1'
    ROBOT_AUTO_KEYWORDS = False

    def __init__(self, API_KEY, server_id, server_domain) -> None:
        """
        The library needs a few arguments in order to work properly:

        - API_KEY which you can retrieve from your mailosaur dashboard

        - server_id which you can retrieve from your mailosaur dashboard

        - server_domain which you can retrieve from your mailosaur dashboard

        Set these arguments when importing the library in the .robot file or set a __init__.robot file with the import and parameters.
        """
        self.mailosaur = MailosaurClient(API_KEY)
        self.server_id = server_id
        self.server_domain = server_domain
        self.criteria = SearchCriteria()

    @keyword
    def email_subject_should_match(self, matcher: str):
        """
        Checks the email subject of the last email received on the current server_domain matches the matcher.
        """
        self.criteria.sent_to = self.server_domain
        last_email = self.mailosaur.messages.get(self.server_id, self.criteria)
        try:
            assert last_email.subject == matcher
        except AssertionError as e:
            raise Exception("AssertionError: '{0}' does not equal '{1}'".format(
                last_email.subject, matcher))

    @keyword
    def email_subject_should_contain(self, matcher: str):
        """
        Checks the email subject of the last email received on the current server_domain contains the matcher.
        """
        self.criteria.sent_to = self.server_domain
        last_email = self.mailosaur.messages.get(self.server_id, self.criteria)
        try:
            assert matcher in last_email.subject
        except AssertionError as e:
            raise Exception("AssertionError: '{0}' does not contain '{1}'".format(
                last_email.subject, matcher))

    @keyword
    def delete_all_emails(self):
        """
        deletes all emails contained in the currently selected server domain.
        """
        self.criteria.sent_to = self.server_domain
        try:
            self.mailosaur.messages.delete_all(self.server_id)
        except Exception as e:
            raise e

    @keyword
    def email_should_have_links(self, links_number: int):
        """
        Checks the last email contains X number of links where X == links_number.
        """
        self.criteria.sent_to = self.server_domain
        last_email = self.mailosaur.messages.get(
            self.server_id, self.criteria)
        links = len(last_email.html.links)
        try:
            assert links == links_number
        except AssertionError as e:
            raise Exception("AssertionError: {0} does not equal {1}".format(
                links, links_number))

    @keyword
    def email_should_have_attachments(self, attachments_number: int):
        """
        Checks the last email contains X number of attachments where X == attachments_number.
        """
        self.criteria.sent_to = self.server_domain
        last_email = self.mailosaur.messages.get(
            self.server_id, self.criteria)
        attachments = len(last_email.attachments)
        try:
            assert attachments == attachments_number
        except AssertionError as e:
            raise Exception("AssertionError: {0} does not equal {1}".format(
                attachments, attachments_number))

    @keyword
    def email_body_should_contain(self, matcher, case_insensitive: bool):
        """
        Checks the last email's body contains a specific string (matcher).

        If case_insensitive is set to True, then case is not checked in the substring.
        """
        self.criteria.sent_to = self.server_domain
        last_email = self.mailosaur.messages.get(
            self.server_id, self.criteria)
        text = last_email.text.body
        if case_insensitive:
            text = text.lower()
            matcher = matcher.lower()
        try:
            assert matcher in text
        except AssertionError as e:
            raise Exception("AssertionError: {0} is not contained {1}".format(
                matcher, text))

    @keyword
    def email_links_should_contain_text(self, text: str):
        """
        Checks if atleast one of the links contained in the last email contains text.
        """
        self.criteria.sent_to = self.server_domain
        last_email = self.mailosaur.messages.get(
            self.server_id, self.criteria)
        links = [link.text for link in last_email.text.links]
        assert any(map(lambda link: text in link, links))

    @keyword
    def email_sender_should_be(self, matcher: str):
        """
        Checks that last email sender matches the given matcher.
        """
        self.criteria.sent_to = self.server_domain
        last_email = self.mailosaur.messages.get(
            self.server_id, self.criteria)
        sender = last_email.sender[0].email
        try:
            assert sender == matcher
        except AssertionError as e:
            raise Exception("AssertionError: '{0}' does not match sender '{1}'".format(
                matcher, sender))
