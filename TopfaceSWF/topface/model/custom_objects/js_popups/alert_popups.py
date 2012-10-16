# coding=utf-8
from selenium.webdriver.support.wait import WebDriverWait
from topface.model.object_model import ObjectModel
from engine.test_failed_exception import TestFailedException
import settings

__author__ = 'ngavrish'

class AlertPopups(ObjectModel):

    _too_short_comment_alert_xpath = ".//div[text()='Ваше сообщение слишком короткое, напишите более развернуто.']//a"
    _delete_message_close = "//div[@role='dialog']//span[@class='ui-dialog-title' and text()='" \
                            + u"Удаление cообщения"\
                            + "']"
    _delete_message_confirm_button = "//div[@id='dialog1']//a[@class='button']"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def too_short_comment_close(self):
        self.logger.log("Closing alert popup for too short comment message")
        try:
            close_link = WebDriverWait(self.browser, settings.wait_for_element_time).\
                            until(lambda driver: driver.find_element_by_xpath(
                                    self._too_short_comment_alert_xpath))
            self.click(close_link)
        except Exception:
            raise TestFailedException("Failed to close too short comment alert")

    def close_delete_message_popup(self):
        self.logger.log("Delete message popup closing")
        try:
            self.click(
                self.get_element_by_xpath(self._delete_message_close))
        except Exception as e:
            raise TestFailedException("Failed to close message delete alert " + e.message)

    def confirm_delete_message_popup(self):
        self.logger.log("Confirming message delete popup")
        try:
            self.click(
                self.get_element_by_xpath(self._delete_message_confirm_button))
        except Exception as e:
            raise TestFailedException("Failed to confirm message deleting " + e.message)