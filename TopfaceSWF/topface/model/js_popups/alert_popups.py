# coding=utf-8
from selenium.webdriver.support.wait import WebDriverWait
from topface.model.model import Model
from engine.test_failed_exception import TestFailedException
import settings

__author__ = 'ngavrish'

class AlertPopups(Model):

    _too_short_comment_alert_xpath = ".//div[text()='Ваше сообщение слишком короткое, напишите более развернуто.']//a"

    def __init__(self,browser,logger):
        Model.__init__(self, browser, logger)
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
            raise TestFailedException("")
