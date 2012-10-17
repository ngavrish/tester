from engine.test_case import TestCase
from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite
import settings
from topface.model.custom_objects.auth import AuthForm
from topface.model.custom_objects.browser_window import BrowserWindow

__author__ = 'ngavrish'

class LoginTestSuite(TestSuite):

    def __init__(self, name):
        TestSuite.__init__(self,name)
        self.browser_name = TestSuite.browser_name
        self.test_cases = []
        self.result = {}

    def run(self):
        self.test_cases = [
                    self.LoginFacebook("LoginFacebook"),
                    self.LoginVkSuccess("LoginVkontakte"),
                    self.LoginMailruSuccess("LoginMailru")
        ]

        for test_case in self.test_cases:
            run_test_results = test_case.run_test(self.browser_name)
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        return {self.__class__.__name__: self.result}


    #noinspection PyMethodOverriding,PyMissingConstructor
    class LoginFacebook(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            # Get local session of firefox
            window = BrowserWindow(browser, logger)
            authForm = AuthForm(browser,logger)

            window.open(settings.target_url)
#            implement URL check

            self.do_method(authForm.click_social,None,"facebook")
            self.do_method(window.switch_to_popup)
            self.do_method(authForm.login_to_fb)
            self.do_method(window.switch_to_root)
            self.do_method(authForm.validate_fb_login_success)
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class LoginVkSuccess(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):
#            raise TestFailedException("Debug Exception")
            window = BrowserWindow(browser, logger)
            authForm = AuthForm(browser,logger)

            window.open(settings.target_url)
#            implement URL check
#            try:
#                assert window.get_current_url() == window.get_unauthorised_url()
#            except AssertionError:
#                raise TestFailedException("Wrong URL")

            self.do_method(authForm.click_social, None, "vkontakte")
            self.do_method(window.switch_to_popup)
            self.do_method(authForm.login_to_vk)
            self.do_method(window.switch_to_root)
            self.do_method(authForm.validate_login_success)
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class LoginMailruSuccess(TestCase):
        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):

            window = BrowserWindow(browser, logger)
            authForm = AuthForm(browser,logger)

            window.open(settings.target_url)
#            implement URL check
#            try:
#                assert window.get_current_url() == window.get_unauthorised_url()
#            except AssertionError:
#                raise TestFailedException("Wrong URL")

            self.do_method(authForm.click_social,None,"mail.ru")
            self.do_method(window.switch_to_popup)
            self.do_method(authForm.login_to_mailru)
            self.do_method(window.switch_to_root)
            self.do_method(authForm.validate_login_success)
            window.close()