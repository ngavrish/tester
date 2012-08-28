# coding=utf-8
from selenium.webdriver.support.wait import WebDriverWait
from topface.model.model import Model
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.buttons import Buttons

__author__ = 'ngavrish'

class Comments(Model):

    _high_mark_comment_xpath = ".//*[@id='extraQuestions']//div[@class='questions-list']/textarea"
    _top_mark_comment_height = "35px"
    _top_mark_initial_value = u'Свой вариант'
    _high_mark_comment_js_selector = "textarea[class='extra-rate-comment-area not-empty']"

    def __init__(self,browser,logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def high_mark(self):
        self.logger.log("Getting high rate mark comment textarea")
        self.browser.implicitly_wait(10)
        try:
            return WebDriverWait(self.browser, settings.wait_for_element_time).\
                        until(lambda driver: driver.find_element_by_xpath(self._high_mark_comment_xpath))
        except Exception:
            raise TestFailedException("Failed to get High Rate comment text area")

    def get_top_mark_comment_height(self):
        return self._top_mark_comment_height

    def is_initial_top_mark_comment(self,comment):
        print "Validating that comment box " + self.get_element_xpath(comment) + " contains initial value"
        self.logger.log("Validating that comment box " + self.get_element_xpath(comment) + " contains initial value")
        try:
            assert self._top_mark_initial_value == comment.get_attribute("placeholder")
        except AssertionError:
            raise TestFailedException("Comment box for high mark doesn't contain correct initial value \r\n")

    def send_comment(self,element,value,comment_type):
        buttons = Buttons(self.browser, self.logger)

        self.logger.log("Typing comment " + comment_type + " with value = " + value)
        element.clear()
        element.send_keys(value)
        self.validate_high_mark_comment_value(value)
        buttons.send_comment(comment_type)

    def validate_high_mark_comment_value(self,value):
        for i in range(10):
            self.browser.implicitly_wait(1)
            if value == self.__get_textarea_value(self._high_mark_comment_js_selector):
                self.logger.log("Validating comment message with value = " + str(value)
                                + " vs " +  self.__get_textarea_value(self._high_mark_comment_js_selector))
                return True
        raise TestFailedException("Failed to validate comment text value" + str(value)
                                    + " vs " +  self.__get_textarea_value(self._high_mark_comment_js_selector))


    def get_high_rate_comment_value(self):
        return self.__get_textarea_value(self._high_mark_comment_js_selector)

    def __get_textarea_value(self,element):
        return self.browser.execute_script(
            "return $(\"" + element + "\").val()")
