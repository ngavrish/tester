from engine.test_failed_exception import TestFailedException
from selenium.webdriver.support.wait import WebDriverWait
import settings
from topface.model.object_model import ObjectModel

__author__ = 'ngavrish'

class DreamsPopup(ObjectModel):

    _close_dreams_xpath = "//div[@class='dream-book-layout']//div[@class='close']"
    _close_dreams_xpath_middle = "//div[@id='dialog1']//div[contains(@class,'close-button')]/a"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def close(self):
        self.logger.log("Closing dreams popup")
        try:
            close_link = WebDriverWait(self.browser, settings.wait_for_element_time).\
                        until(lambda driver: driver.find_element_by_xpath(self._close_dreams_xpath))
            self.click(close_link)
            self.click(
                self.get_element_by_xpath(self._close_dreams_xpath_middle))
        except Exception:
            print "Couldn't find dreams popup"