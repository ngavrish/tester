from engine.test_case import TestCase
from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite
import settings
from topface.model.auth import AuthForm
from topface.model.browser_window import BrowserWindow

__author__ = 'ngavrish'

#noinspection PyMethodOverriding
class LoginTestSuite(TestSuite):

    def __init__(self):
        self.test_cases = []
        self.result = {}

    def run(self):
        self.test_cases = [
                    self.LoginFacebook("LoginFacebookSuccessTest"),
                    self.LoginVkSuccess("LoginVkontakteSuccessTest"),
#                    self.LoginMailruSuccess("LoginMailruSuccessTest")
        ]

        for test_case in self.test_cases:
            run_test_results = test_case.run_test()
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        return {self.__class__.__name__: self.result}


    #noinspection PyMethodOverriding,PyMissingConstructor
    class LoginFacebook(TestCase):
        """

        """
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            # Get local session of firefox
            window = BrowserWindow(browser, logger)
            authForm = AuthForm(browser,logger)

            window.open(settings.target_url)
            try:
                assert window.get_current_url() == window.get_unauthorised_url()
            except AssertionError:
                raise TestFailedException("Wrong URL")

            authForm.click_social("facebook")
            window.switch_to_popup()
            authForm.login_to_fb()
            window.switch_to_root()
            authForm.validate_fb_login_success()
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class LoginVkSuccess(TestCase):
        """

        """
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):
#            raise TestFailedException("Debug Exception")
            window = BrowserWindow(browser, logger)
            authForm = AuthForm(browser,logger)

            window.open(settings.target_url)
            try:
                assert window.get_current_url() == window.get_unauthorised_url()
            except AssertionError:
                raise TestFailedException("Wrong URL")

            authForm.click_social("vkontakte")
            window.switch_to_popup()
            authForm.login_to_vk()
            window.switch_to_root()
            authForm.validate_login_success()
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class LoginMailruSuccess(TestCase):
        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):

            window = BrowserWindow(browser, logger)
            authForm = AuthForm(browser,logger)

            window.open(settings.target_url)
            try:
                assert window.get_current_url() == window.get_unauthorised_url()
            except AssertionError:
                raise TestFailedException("Wrong URL")

            authForm.click_social("mail.ru")
            window.switch_to_popup()
            authForm.login_to_mailru()
            window.switch_to_root()
            authForm.validate_login_success()
            window.close()