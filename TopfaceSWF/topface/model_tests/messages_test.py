# coding=utf-8
from time import sleep
from engine.test_suite import TestSuite
from engine.test_case import TestCase
from topface.model.auth import AuthForm
from topface.model.browser_window import BrowserWindow
from topface.model.navigation import Navigation
from topface.model.messanger import Messenger
from topface import profiling_events

__author__ = 'ngavrish'


class MessagesTestSuite(TestSuite):

    def __init__(self):
        self.test_cases = []
        self.result = {}

    def run(self):
        """
        """
        self.test_cases = [
            self.MessagesFacebookFactTest("MessagesFacebookFactTest")
        ]
        for test_case in self.test_cases:
            run_test_results = test_case.run_test()
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        print "Test cases amount = " + str(len(self.result))
        return {self.__class__.__name__: self.result}

    class MessagesFacebookFactTest(TestCase):
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
            print "User 1 message validation finished successfully"

            self.do_method(auth.login_with_fb_full_scale,profiling_events.events[profiling_events.login_event],auth.User2)
            sleep(2)
            navigation.goto_side_menu_item(u"Сообщения")
            sleep(2)
            navigation.validate_in_tab(u"Новые")
            messenger.validate_last_message_in_feed_fb(output_message)
            navigation.goto_tab_menu_item(u"Входящие")
            messenger.validate_last_message_in_feed_fb(output_message)


            window.close()
