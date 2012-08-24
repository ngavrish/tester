from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite

__author__ = 'user'

class BrowserWindow:
    """

    """
    __unauthorised_url = "http://topface.com/ru/auth/?url=%2F"
    __root_window = None
    __windows_list = []

    def __init__(self,browser,logger):
        self.browser = browser
        self.logger = logger

    def open(self,url):
        try:
            self.browser.get(url)
            self.logger.log("Open " + TestSuite.browser_name + " at " + url)
            self.__root_window = self.browser.current_window_handle
        except Exception as e:
            raise TestFailedException("Failed to open browser on URL = " + url + " : " + e.message)

    def get_current_url(self):
        self.logger.log("Validating current URL = " + self.browser.current_url)
        return self.browser.current_url

    def get_unauthorised_url(self):
        return self.__unauthorised_url

    def switch_to_popup(self):
        try:
            # click on the link that opens a new window
            self.__windows_list = self.browser.window_handles
            # before the pop-up window closes
            self.__windows_list.remove(self.__root_window)
            self.browser.switch_to_window(self.__windows_list.pop())
            self.logger.log("Switched to window " + self.browser.title)
        except Exception as e:
            raise TestFailedException("Failed to switch to popup " + e.message)

    def switch_to_root(self):
        try:
            self.browser.switch_to_window(self.__root_window)
            self.logger.log("Switched to window " + self.browser.title)
        except Exception as e:
            raise TestFailedException("Failed to switch back to root browser window: " + e.message)

    def close(self):
        try:
            self.logger.log("END TEST")
            self.browser.close()
        except Exception as e:
            raise TestFailedException("Failed to close browser " + e.message)