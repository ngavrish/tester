# coding=utf-8
from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite
from selenium.webdriver.support.wait import WebDriverWait
from topface.model.model import Model
import settings

__author__ = 'ngavrish'

class BrowserWindow(Model):
    """

    """
    _social_switcher_wrapper_xpath = "//div[@class='auth-form']"
    _unauthorised_url = "http://topface.com/ru/auth/?url=%2F" #"http://topface.com/ru/"
    _exit_link_id = "exit"
    _root_window = None
    _windows_list = []

    def __init__(self, browser, logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def open(self,url):
        try:
            self.browser.get(url)
            self.logger.log("Open " + TestSuite.browser_name + " at " + url)
            self._root_window = self.browser.current_window_handle
        except Exception as e:
            raise TestFailedException("Failed to open browser on URL = " + url + " : " + e.message)

    def get_current_url(self):
        self.logger.log("Validating current URL = " + self.browser.current_url)
        return self.browser.current_url

    def get_unauthorised_url(self):
        return self._unauthorised_url

    def switch_to_popup(self):
        try:
            # click on the link that opens a new window
            self._windows_list = self.browser.window_handles
            self._root_window = self.browser.current_window_handle
            print "Windwos list = " + str(self.browser.window_handles)
            # before the pop-up window closes
            print "Root window = " + self._root_window
            if self._root_window in self._windows_list:
                print "HIT"
            self._windows_list.remove(self._root_window)
            self.browser.switch_to_window(self._windows_list.pop())
            self.logger.log("Switched to window " + self.browser.title)
        except Exception as e:
            raise TestFailedException("Failed to switch to popup " + e.message)

    def switch_to_root(self,root=None):
        try:
        #            if self.browser.title.find(u"Топфейс") < 0:
            if root is not None:
                self._root_window = root
            print "root window " + str(self._root_window)
            self.browser.switch_to_window(self._root_window)
            print "current window = " + str(self.browser.current_window_handle)
            self.logger.log("Switched to window " + self.browser.title)
        except Exception as e:
            raise TestFailedException("Failed to switch back to root browser window: " + e.message)

    def logout(self):
        self.logger.log("Logout")
        try:
            self.click(self.get_element_by_id(self._exit_link_id))
            WebDriverWait(self.browser, settings.wait_for_element_time).\
                        until(lambda driver: driver.find_element_by_xpath(self._social_switcher_wrapper_xpath))
        except Exception:
            raise TestFailedException("Failed to logout")

    def close(self):
        try:
            self.logger.log("END TEST")
            self.browser.close()
        except Exception as e:
            raise TestFailedException("Failed to close browser " + e.message)