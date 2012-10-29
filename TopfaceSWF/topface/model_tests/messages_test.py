# coding=utf-8
from time import sleep
from engine.test_suite import TestSuite
from engine.test_case import TestCase
from topface import profiling_events
from topface.model.custom_objects.auth import AuthForm
from topface.model.custom_objects.browser_window import BrowserWindow
from topface.model.custom_objects.messanger import Messenger
from topface.model.custom_objects.navigation import Navigation

__author__ = 'ngavrish'


class MessagesTestSuite(TestSuite):

    def __init__(self,name):
        TestSuite.__init__(self,name)
        self.browser_name = TestSuite.browser_name
        self.test_cases = []
        self.result = {}

    def run(self):
        """
        """
        self.test_cases = [
            self.MessagesFacebookSentTest("MessagesFacebookSentTest"),
            self.MessagesFacebookValidateTest("MessagesFacebookValidateTest")
        ]
        for test_case in self.test_cases:
            run_test_results = test_case.run_test(self.browser_name)
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        print "Test cases amount = " + str(len(self.result))
        return {self.__class__.__name__: self.result}

#    MESSAGES FACT TEST - SINGLE TESTCASE IN SEVERAL TESTMETHODS
    class MessagesFacebookSentTest(TestCase):
        """
        No UI validation stuff mostly
        Just hard simple business-logic
        """
        _root_window = ""
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            auth = AuthForm(self.browser, self.logger)
            window = BrowserWindow(self.browser,self.logger)
            navigation = Navigation(self.browser,self.logger)
            messenger = Messenger(self.browser, self.logger)

            output_message = u"Привет!"

            self.do_method(auth.login_with_fb_full_scale,profiling_events.login_event,auth.User1)
            window.open(auth.User2.profile_url)
            navigation.goto_messenger_from_profile()
#            No UI validation
            self._root_window = self.browser.current_window_handle
            messenger.send_and_validate_message(output_message)
            window.switch_to_popup()
            navigation.goto_side_menu_item(u"Сообщения")
            navigation.goto_tab_menu_item(u"Отправленные")
            messenger.delete_last_message_from_output_feed_fb(output_message)
            window.logout()

    class MessagesFacebookValidateTest(TestCase):
        """
        No UI validation stuff mostly
        Just hard simple business-logic
        """
        _root_window = ""
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            auth = AuthForm(self.browser, self.logger)
            window = BrowserWindow(self.browser,self.logger)
            navigation = Navigation(self.browser,self.logger)
            messenger = Messenger(self.browser, self.logger)

            print "User 1 message validation finished successfully"

            output_message = u"Привет!"
            self.do_method(auth.login_with_fb_full_scale,profiling_events.events[profiling_events.login_event],auth.User2)
            sleep(2)
            navigation.goto_side_menu_item(u"Сообщения")
            sleep(2)
            navigation.validate_in_tab(u"Новые")
            messenger.validate_last_message_in_feed_fb(output_message)
            navigation.goto_tab_menu_item(u"Входящие")
            messenger.validate_last_message_in_feed_fb(output_message)
            window.close()

#    /MESSAGES FACT TEST - SINGLE TESTCASE IN SEVERAL TESTMETHODS