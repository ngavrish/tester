# coding=utf-8
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.custom_objects.buttons import Buttons
from topface.model.object_model import ObjectModel

__author__ = 'ngavrish'

class Comments(ObjectModel):

    _high_mark_comment_xpath = ".//*[@id='extraQuestions']//div[@class='questions-list']/textarea"
    _top_mark_comment_height = "35px"
    _top_mark_initial_value = u'Свой вариант'
    _high_mark_comment_js_selector = "textarea[class='extra-rate-comment-area not-empty']"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def get_high_mark(self):
        self.logger.log("Getting high rate mark comment textarea")
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
        self.enter_text(element,value)
        self.validate_high_mark_comment_value(value)
        buttons.send_comment(comment_type)

    def validate_high_mark_comment_value(self,value):
        self.logger.log("Validating comment message with value = " + str(value)
                        + " vs " +  str(self.__get_textarea_value(self._high_mark_comment_js_selector)))
        try:
            WebDriverWait(self.browser, settings.wait_for_element_time).\
                        until(self.__get_high_mark_height_occurences())
        except Exception:
#            WebDriverWait doesn't work as documented. If method in until() returns true, it fails either way
#            only works when using lambda driver searching element in web interface function
#            so hacking a bit
            sleep(1)
            if self.get_high_mark().get_attribute("style").count(self.get_top_mark_comment_height()) <= 0:
                print "Failed to change comment box style"
                raise TestFailedException("Comment text area didn't change style")

        try:
            print "Expected: " + value
            print "Recieved: " + self.__get_textarea_value(self._high_mark_comment_js_selector)
            assert value == self.__get_textarea_value(self._high_mark_comment_js_selector)
        except Exception:
            print "Text validation failed"
            raise TestFailedException("Failed to validate comment text value")

    def get_high_rate_comment_value(self):
        return self.__get_textarea_value(self._high_mark_comment_js_selector)

    def __get_textarea_value(self,element):
        return self.browser.execute_script(
            "return $(\"" + element + "\").val()")

    def __get_high_mark_height_occurences(self):
        return self.get_high_mark().get_attribute("style").count(self.get_top_mark_comment_height()) > 0