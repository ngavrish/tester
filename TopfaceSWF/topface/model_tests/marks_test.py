# coding=utf-8
from __future__ import division
from datetime import datetime
from engine.test_case import TestCase
from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite
import math
from topface.model.auth import AuthForm
from topface.model.buttons import Buttons
from topface.model.marks import Marks
from topface.model.navigation import Navigation
import settings
from topface.model.browser_window import BrowserWindow
from topface.model.comments import Comments
from topface.model.energy import Energy
from topface.model.js_popups.alert_popups import AlertPopups

__author__ = 'ngavrish'

#noinspection PyMethodOverriding
class MarksTestSuite(TestSuite):

    def __init__(self):
        self.test_cases = []
        self.result = []

    def run(self):
        """

        """
        self.test_cases = [
            self.MarkUserOne2Eight("MarkUserOne2EightTest"),
            self.MarkUserTopUserMessage("MarkUserTopUserMessage"),#has bug
            self.MarkUserTopStandartMessages("MarkUserTopStandartMessages"),
            self.MarkEnergyChargeTest("MarkEnergyChargeTest"), #has bug
            self.MarkFactTest("MarkFactTest")]

        for test_case in self.test_cases:
            self.result = test_case.run_test()
        return {self.__class__.__name__: self.result}

        #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkUserOne2Eight(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)

            auth.login_with_fb_full_scale()

            minor_marks = marks.get_minor_marks()
            for mark in minor_marks:
                photo_href1 = marks.get_photo2mark_href()
                marks.click(mark)
                photo_href2 = marks.get_photo2mark_href()
                try:
                    assert photo_href1 != photo_href2
                except AssertionError:
                    raise TestFailedException("User haven't been changed after marking")
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkUserTopUserMessage(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
            comments = Comments(self.browser, self.logger)
            alerts = AlertPopups(self.browser, self.logger)

            auth.login_with_fb_full_scale()

            major_marks = marks.get_major_marks()

            for mark in major_marks:
                photo_href1 = marks.get_photo2mark_href()
                marks.click(mark)
                top_mark_comment = comments.high_mark()
                comments.is_initial_top_mark_comment(top_mark_comment)
                if top_mark_comment.get_attribute("style") != "":
                    raise TestFailedException("Top Mark comment style exists but shouldn't")
                comments.click(top_mark_comment)
                #                reload comment element from web interface
                top_mark_comment = comments.high_mark()

                print top_mark_comment.get_attribute("style")

                if top_mark_comment.get_attribute("style").count(comments.get_top_mark_comment_height()) <= 0:
                    raise TestFailedException("Top Mark comment element doesn't contain needed style=height:" +
                                              comments.get_top_mark_comment_height())
                #                validate that comment textarea still contains initial text
                #                BUG NEXT LINE
                #                comments.is_initial_top_mark_comment(top_mark_comment)
                #                send single key
                comments.send_comment(top_mark_comment, u'1', "topmark")
                alerts.too_short_comment_close()
                comments.click(top_mark_comment)
                comments.send_comment(top_mark_comment, u"Привет", "topmark")
                photo_href2 = marks.get_photo2mark_href()
                try:
                    assert photo_href1 != photo_href2
                except AssertionError:
                    raise TestFailedException("User haven't been changed after marking")

            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkUserTopStandartMessages(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
            comments = Comments(self.browser, self.logger)
            buttons = Buttons(self.browser, self.logger)

            auth.login_with_fb_full_scale()

            major_marks = marks.get_major_marks()
            for mark in major_marks:
                photo_href1 = marks.get_photo2mark_href()
                marks.click(mark)
                compliments = marks.get_random_compliments()
                compliments_error_threshold = math.ceil(len(compliments)/2)
                print "Compliments change error threshold = " + str(compliments_error_threshold)
                error_count = 0
                for compliment in compliments:
                    marks.click(compliment)
                    try:
                        comments.validate_high_mark_comment_value(compliment.text)
                    except Exception:
                        error_count += 1
                    if error_count >= compliments_error_threshold:
                        raise TestFailedException("Faield standart comment sending functionality. " +\
                                                  "Error count during sending comments = " + str(error_count))
                buttons.send_comment("topmark")
                photo_href2 = marks.get_photo2mark_href()
                try:
                    print photo_href1
                    print photo_href2
                    assert photo_href1 != photo_href2
                except AssertionError:
                    raise TestFailedException("User photo hasn't changed")
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

            auth.login_with_fb_full_scale()
            initial_energy_value = energy.get_profile_percent_value()
            marks_left_till_plus = marks.get_marks_left_till_energy_plus()
            marks_left = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
            mark_seven = marks.get_mark_by_value(7)

            print "Marks left = " + str(marks_left)

            for i in range(marks_left):
                print "step " + str(i)
                marks_left_till_plus = marks.get_marks_left_till_energy_plus()
                marks_left_new_before_click = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
                marks.click(mark_seven)
                marks_left_till_plus = marks.get_marks_left_till_energy_plus()
                marks_left_new_after_click = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
                try:
                    assert marks_left_new_after_click == (marks_left_new_before_click - 1)
                except AssertionError:
                    raise TestFailedException("Click wrongly changed amount of left clicks on step " + str(i))
            try:
                print initial_energy_value
                print energy.get_profile_percent_value()
                assert initial_energy_value == energy.get_profile_percent_value() - 3
            except AssertionError:
                raise TestFailedException("Failed to add correct energy amount")
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkFactTest(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            marks = Marks(self.browser, self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
            navigation = Navigation(self.browser,self.logger)
#       login as user1
            self.logger.log("\r\nLogin as User1\r\n")
            auth.login_with_fb_full_scale(auth.User1)
            window.open(AuthForm.User2.profile_url)
            marks.click(
                marks.get_mark_by_value(1)
            )
            marks.validate_profile_mark_sent()
            window.logout()

            self.logger.log("\r\nLogin as User2\r\n")
            auth.login_with_fb_full_scale(auth.User2)
            navigation.goto_side_menu_item(u"Оценки")
            marks.validate_new_mark_in_feed(AuthForm.User1.profile_url,datetime.now().strftime("%d"))
            marks.rate_answer(AuthForm.User1.profile_url)
            window.logout()

            self.logger.log("\r\nLogin as User1\r\n")
            auth.login_with_fb_full_scale(auth.User1)
            navigation.goto_side_menu_item(u"Оценки")
            marks.validate_new_mark_in_feed(AuthForm.User2.profile_url,datetime.now().strftime("%d"))
            window.close()
