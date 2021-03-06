# coding=utf-8
from __future__ import division
from datetime import datetime
from engine.test_case import TestCase
from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite
from topface.model.custom_objects.auth import AuthForm
from topface.model.custom_objects.marks import Marks
from topface.model.custom_objects.navigation import Navigation
import settings
from topface.model.custom_objects.browser_window import BrowserWindow
from topface.model.custom_objects.energy import Energy
from topface import profiling_events

__author__ = 'ngavrish'

#noinspection PyMethodOverriding
class MarksTestSuite(TestSuite):

    def __init__(self,name):
        TestSuite.__init__(self,name)
        self.browser_name = TestSuite.browser_name
        self.test_cases = []
        self.result = {}

    def run(self):
        """

        """
        self.test_cases = [
           self.MarkUserOne2Eight("MarkUserOne2EightTest"),
           self.MarkUserTopUserMessage("MarkUserTopUserMessage"),#has bug
           self.MarkUserTopStandartMessages("MarkUserTopStandartMessages"),
           self.MarkEnergyChargeTest("MarkEnergyChargeTest"), #has bug
           self.MarkFactTest_MarkUser2("MarkFactTest_MarkUser2"),
           self.MarkFactTest_ValidateAndMarkBackUser1("MarkFactTest_ValidateAndMarkBackUser1"),
           self.MarkFactTest_ValidateUser1("MarkFactTest_ValidateUser1"),
           self.ValidateUnquieUsersInsearch("UniqueUsersValidation")
        ]

        for test_case in self.test_cases:
            run_test_results = test_case.run_test(self.browser_name)
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        return {self.__class__.__name__: self.result}

        #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkUserOne2Eight(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):

            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)

            self.do_method(auth.login_with_fb_full_scale,profiling_events.login_event)
            minor_marks = marks.get_minor_marks()
            for mark in minor_marks:
                self.do_method(marks.mark_and_validate_mark,None,mark)
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkUserTopUserMessage(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):

            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)

            self.do_method(auth.login_with_fb_full_scale,profiling_events.login_event)
            major_marks = marks.get_major_marks()
            self.do_method(marks.mark_major_marks_custom_comment,None,major_marks)

            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkUserTopStandartMessages(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):

            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)

            self.do_method(auth.login_with_fb_full_scale,profiling_events.login_event)
            major_marks = marks.get_major_marks()
            self.do_method(marks.mark_major_marks_standart_comment,None,major_marks)
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkEnergyChargeTest(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):

            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
            energy = Energy(self.browser, self.logger)

            self.do_method(auth.login_with_fb_full_scale,profiling_events.login_event)
            initial_energy_value = energy.get_profile_percent_value()
            marks_left_till_plus = marks.get_marks_left_till_energy_plus()
            marks_left = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]

            print "Marks left = " + str(marks_left)

            for i in range(marks_left):
                print "step " + str(i)
                self.do_method(marks.marking_made_closer_to_more_energy,None,marks_left_till_plus,i)
            try:
                self.logger.log("Initial egergy value = " + str(initial_energy_value))
                print energy.get_profile_percent_value()
                assert initial_energy_value == energy.get_profile_percent_value() - 3
            except AssertionError:
                raise TestFailedException("Failed to add correct energy amount")
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor

#    SINGLE TESTCASE IN THREE TEST METHODS
    class MarkFactTest_MarkUser2(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):

            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
#       login as user1
            self.logger.log("\r\nLogin as User1\r\n")
            self.do_method(auth.login_with_fb_full_scale,profiling_events.login_event,auth.User1)
            self.do_method(window.open,None,AuthForm.User2.profile_url)
            marks.click(
                marks.get_mark_by_value(1)
            )
            self.do_method(marks.validate_profile_mark_sent)
            window.close()

    class MarkFactTest_ValidateAndMarkBackUser1(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):

            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
            navigation = Navigation(self.browser,self.logger)
            #       login as user1
            self.logger.log("\r\nLogin as User2\r\n")

            self.do_method(auth.login_with_fb_full_scale,profiling_events.events[profiling_events.login_event],auth.User2)
            self.do_method(navigation.goto_side_menu_item,None,u"Оценки")
            self.do_method(marks.validate_new_mark_in_feed,None,AuthForm.User1.profile_url_fb,datetime.now().strftime("%d"))
            self.do_method(marks.rate_answer,None,AuthForm.User1.profile_url_fb)
            window.close()

    class MarkFactTest_ValidateUser1(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):

            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
            navigation = Navigation(self.browser,self.logger)
            #       login as user1
            self.logger.log("\r\nLogin as User1\r\n")

            self.do_method(auth.login_with_fb_full_scale,profiling_events.events[profiling_events.login_event],auth.User1)
            self.do_method(navigation.goto_side_menu_item,None,u"Оценки")
            self.do_method(marks.validate_new_mark_in_feed,None,AuthForm.User2.profile_url,datetime.now().strftime("%d"))
            window.close()
#    /SINGLE TESTCASE IN THREE TEST METHODS

    class ValidateUnquieUsersInsearch(TestCase):
        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):
            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)

            self.do_method(auth.login_with_fb_full_scale,profiling_events.events[profiling_events.login_event],auth.User1)
            marked_users = [marks.get_photo2mark_href()]
            for i in range(marks.unique_amount):
                marks.like()
                href2like = marks.get_photo2mark_href()
                if href2like in marked_users:
                    print marked_users
                    print href2like
                    raise TestFailedException("Found duplicate user in main search")
                marked_users.append(href2like)
                marks.mark()
                href2like = marks.get_photo2mark_href()
                if href2like in marked_users:
                    self.logger.log("Duplicate user = " + href2like + " found in list " + str(marked_users))
                    raise TestFailedException("Found duplicate user in main search")
                marked_users.append(href2like)
            window.close()