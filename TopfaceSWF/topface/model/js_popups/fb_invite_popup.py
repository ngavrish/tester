from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import settings

__author__ = 'user'

class FbInviteFriendsPopup:

    __close_xpath = "//div[@id='fb-root']/div[2]/a"
    __id = "fb-root"

    def __init__(self,browser,logger):
        self.browser = browser
        self.logger = logger

    def close(self):
        try:
            self.logger.log("Searching for invite friends popup")
            closer = WebDriverWait(self.browser, settings.wait_for_element_time).until(
                lambda driver: driver.find_element_by_xpath(self.__close_xpath))
            closer.click()
        except NoSuchElementException:
            self.logger.log("Invite friends popup not found")
        except TimeoutException:
            self.logger.log("Invite friends popup not found")

