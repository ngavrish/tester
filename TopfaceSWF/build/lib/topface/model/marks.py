from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.model import Model

__author__ = 'ngavrish'

class Marks(Model):

    _star_box_id = "starBox"
    _minor_marks_xpath = ".//*[@id='starBox']//a[@data-index!='0' " \
                            "and @data-index!='9' and @data-index!='10']"
    _major_marks_xpath = ".//*[@id='starBox']//a[@data-index='9' or @data-index='10']"
    _photo2mark_xpath = "//div[@id='userPhotoLayout']/a"
    _random_compliments_xpath = ".//*[@id='extraQuestions']//div[@class='questions-list']//label[contains(@class,'message-variant random-compliments')]"

    def __init__(self,browser,logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def star_box(self):
        self.logger.log("Waiting for element with ID = " + self._star_box_id)
        try:
            return WebDriverWait(self.browser, settings.wait_for_element_time).\
                    until(lambda driver: driver.find_element_by_id(self._star_box_id))
        except Exception:
            raise TestFailedException("Failed to get STARBOX - the marks wrapper")

    def get_minor_marks(self):
        self.logger.log("Get all minor marks - marks from 1 to 8")
        try:
            return WebDriverWait(self.browser,settings.wait_for_element_time).\
                    until(lambda driver: driver.find_elements_by_xpath(self._minor_marks_xpath))
        except Exception:
            raise TestFailedException("Failed to get minor marks")

    def get_major_marks(self):
        self.logger.log("Getting major marks - marks from 9 to 10")
        try:
            return WebDriverWait(self.browser,settings.wait_for_element_time).\
                    until(lambda driver: driver.find_elements_by_xpath(self._major_marks_xpath))
        except Exception:
            raise TestFailedException("Failed to get major marks")

    def get_mark_by_value(self,value):
        self.logger.log("Getting mark with value = " + value)
        try:
            return WebDriverWait(self.browser,settings.wait_for_element_time).\
                    until(lambda driver: driver.find_element_by_xpath(".//*[@id='starBox']//a[@data-index='"+value+"']"))
        except Exception:
            raise TestFailedException("Failed to get Mark by value")

    def get_photo2mark_href(self):
        self.logger.log("Get photo to mark")
        try:
            return WebDriverWait(self.browser,settings.wait_for_element_time).\
                    until(lambda driver: driver.find_element_by_xpath(self._photo2mark_xpath).get_attribute("href"))
        except Exception:
            raise TestFailedException("Failed to get photo href to mark")

    def get_random_compliments(self):
        self.logger.log("Getting random compliments elements")
        try:
            return  WebDriverWait(self.browser, settings.wait_for_element_time).\
                                until(lambda driver: driver.find_elements_by_xpath(self._random_compliments_xpath))
        except Exception:
            raise TestFailedException("Failed to get random compliments elements")

    def click(self, element):
        try:
            self.logger.log("Clicking on mark " + self.get_element_xpath(element))
            hover = ActionChains(self.browser).move_to_element(element)
            hover.perform()
            element.click()
        except Exception:
            raise TestFailedException("Failed to click on element " + self.get_element_xpath(element))

