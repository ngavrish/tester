# coding=utf-8
from time import sleep
from topface.model.model import Model
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.js_popups.alert_popups import AlertPopups

__author__ = 'ngavrish'

class Messenger(Model):

    _message_box_xpath = "//div[@id='sendMessageForm']//textarea"
    _send_message_button_xpath = ".//*[@id='sendMessageForm']//button"
    _last_message_text = "//div[@class='messages-wrapper']//ul/li[last()]//div[contains(@class,'message')]"
    _1st_message_in_feed_notext_xpath_fb = "//div[@id='comments']//div[contains(@class,'commentContainer')][1]//div[@class='text']//span[text()='"

    def __init__(self,browser,logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def send_and_validate_message(self,text):
        message_box = self.wait4xpath(settings.wait_for_element_time, self._message_box_xpath)
        self.click(message_box)
        self.enter_text(message_box,text)
        self.click(
            self.get_element_by_xpath(
                self._send_message_button_xpath))
        try:
            print_failed = False
            try:
                print "TEXT = " + text
                print "UI MESSAGE = " + self.get_element_by_xpath(self._last_message_text).text
            except UnicodeEncodeError as e:
                print_failed = True
                print "Print Message error = " + e.message
            self.logger.log(u"Comparing" + self.get_element_by_xpath(self._last_message_text).text + " vs " + text)
            if not print_failed:
                assert self.get_element_by_xpath(self._last_message_text).text == text
        except AssertionError as e:
            raise TestFailedException("Message body sent is wrong: " + e.message)

    def validate_last_message_in_feed_fb(self,text):
        self.logger.log("Validate last message in feed")
        self.hover(self.get_element_by_xpath(
            self._1st_message_in_feed_notext_xpath_fb + text + "']"
        ))

    def delete_last_message_from_output_feed_fb(self,text):
        alert_popups = AlertPopups(self.browser, self.logger)
        print "Last message close button xpath = " + self.get_message_link_delete_from_feed_xpath_fb(text)
        close = self.get_element_by_xpath(self.get_message_link_delete_from_feed_xpath_fb(text))
#        no validation that close icon appeared
        self.hover(self.get_element_by_xpath(
            self._1st_message_in_feed_notext_xpath_fb + text + "']"
        ))
        print 1
        print 2
        self.click(close)
        alert_popups.close_delete_message_popup()
        alert_popups.confirm_delete_message_popup()

    def get_message_link_delete_from_feed_xpath_fb(self, text):
        return self._1st_message_in_feed_notext_xpath_fb + text + "']/../../../a[contains(@class,'removeComment')]"

