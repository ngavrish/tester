from selenium.webdriver.support.wait import WebDriverWait
import settings
from topface.model.model import Model

__author__ = 'ngavrish'


class SexyPopup(Model):

    _close_sexy_xpath = "//div[@role='dialog']//a[contains(@class,'corner-all') and @role='button']"

    def __init__(self,browser,logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def close(self):
        self.logger.log("Closing sexy popup")
        try:
            close_link = WebDriverWait(self.browser, settings.wait_for_element_time).\
                        until(lambda driver: driver.find_element_by_xpath(self._close_sexy_xpath))
            self.click(close_link)
        except Exception:
            print "Couldn't find sexy popup"