from selenium.webdriver.support.wait import WebDriverWait
import settings

__author__ = 'user'

class Marking:

    __star_box_id = "starBox"

    def __init__(self,browser,logger):
        self.browser = browser
        self.logger = logger

    def star_box(self):
        self.logger.log("Waiting for element with ID = " + self.__star_box_id)
        return WebDriverWait(self.browser, settings.wait_for_element_time).until(lambda driver: driver.find_element_by_id(self.__star_box_id))

