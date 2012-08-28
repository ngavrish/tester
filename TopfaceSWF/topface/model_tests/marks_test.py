# coding=utf-8
from engine.test_case import TestCase
from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite
from topface.model.auth import AuthForm
from topface.model.buttons import Buttons
from topface.model.marks import Marks
import settings
from topface.model.browser_window import BrowserWindow
from topface.model.comments import Comments
from topface.model.js_popups.alert_popups import AlertPopups

__author__ = 'ngavrish'

#noinspection PyMethodOverriding
class MarksTestSuite(TestSuite):
    def run(self):
        """

        """
        test_cases = [
                    #self.MarkUserOne2Eight("MarkUserOne2EightTest"),
                    #self.MarkUserTopUserMessage("MarkUserTopUserMessage"),
                    self.MarkUserTopStandartMessages("MarkUserTopStandartMessages")]
#                      self.LoginVkSuccess("LoginVkontakteSuccessTest"),
#                      self.LoginMailruSuccess("LoginMailruSuccessTest")]
        for test_case in test_cases:
            test_case.run_test()
    #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkUserOne2Eight(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            marks = Marks(self.browser,self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)

            auth.login_with_facebook()

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
            marks = Marks(self.browser,self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
            comments = Comments(self.browser,self.logger)
            alerts = AlertPopups(self.browser,self.logger)

            auth.login_with_facebook()

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
                comments.send_comment(top_mark_comment,u'1',"topmark")
                alerts.too_short_comment_close()
                comments.click(top_mark_comment)
                comments.send_comment(top_mark_comment,u"Привет","topmark")
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
            marks = Marks(self.browser,self.logger)
            window = BrowserWindow(self.browser, self.logger)
            auth = AuthForm(self.browser, self.logger)
            comments = Comments(self.browser,self.logger)
            buttons = Buttons(self.browser,self.logger)
            alerts = AlertPopups(self.browser,self.logger)

            auth.login_with_facebook()

            major_marks = marks.get_major_marks()
            for mark in major_marks:
                photo_href1 = marks.get_photo2mark_href()
                marks.click(mark)
                top_mark_comment = comments.high_mark()
                compliments = marks.get_random_compliments()
                for compliment in compliments:
                    marks.click(compliment)
                    print compliment.text
                    comments.validate_high_mark_comment_value(compliment.text)

                buttons.send_comment("topmark")
                photo_href2 = marks.get_photo2mark_href()
                try:
                    assert photo_href1 == photo_href2
                except AssertionError:
                    raise TestFailedException("User photo hasn't changed")
            window.close()
#
#            profileLink2 = self.browser.find_element_by_xpath("//div[@id='userPhotoLayout']/a").get_attribute("href")
#            print "Element = " + mark.get_attribute("innerHTML")
#
#            assert profileLink1 != profileLink2
#
#            self.browser.find_element_by_id("exit").click()
#            self.browser.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MarkEnergyChargeTest(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)


        def run(self, browser, logger):
            pass
#            percent_energy = float(self.browser\
#                                   .find_element_by_xpath(".//*[@id='sideMenu']//div[contains(@class,'val')]")\
#                                   .get_attribute("innerHTML")[:-1]\
#            .replace(",", "."))
#            marks_left_till_plus = self.browser.\
#            find_element_by_xpath(
#                "//div[@id='user-rates-bonus-block']//span[@class='power-bonus-message']").get_attribute(
#                "innerHTML")
#            marks_left = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
#
#            mark_five = self.browser.find_element_by_xpath(".//*[@id='starBox']//a[@data-index='5']")
#
#            for i in range(marks_left):
#                marks_left_till_plus = self.browser.\
#                find_element_by_xpath(
#                    "//div[@id='user-rates-bonus-block']//span[@class='power-bonus-message']").get_attribute(
#                    "innerHTML")
#                marks_left_new_before_click = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
#                hover = ActionChains(self.browser).move_to_element(mark_five)
#                hover.perform()
#                mark_five.click()
#                print i
#                marks_left_till_plus = self.browser.\
#                find_element_by_xpath(
#                    "//div[@id='user-rates-bonus-block']//span[@class='power-bonus-message']").get_attribute(
#                    "innerHTML")
#                marks_left_new_after_click = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
#                assert marks_left_new_after_click == (marks_left_new_before_click - 1)
#            assert percent_energy == float(self.browser\
#                                           .find_element_by_xpath(".//*[@id='sideMenu']//div[contains(@class,'val')]")\
#                                           .get_attribute("innerHTML")[:-1]\
#            .replace(",", ".")) + 3
#            self.browser.close()

    #noinspection PyMethodOverriding,PyMissingConstructor