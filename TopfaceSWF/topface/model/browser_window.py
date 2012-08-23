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
        self.browser.get(url)
        self.logger.log("Open " + TestSuite.browser_name + " at " + url)
        self.__root_window = self.browser.current_window_handle

    def get_current_url(self):
        self.logger.log("Validating current URL = " + self.browser.current_url)
        return self.browser.current_url

    def get_unauthorised_url(self):
        return self.__unauthorised_url

    def switch_to_popup(self):
        # click on the link that opens a new window
        self.__windows_list = self.browser.window_handles
        # before the pop-up window closes
        self.__windows_list.remove(self.__root_window)
        self.browser.switch_to_window(self.__windows_list.pop())
        self.logger.log("Switched to window " + self.browser.title)

    def switch_to_root(self):
        self.browser.switch_to_window(self.__root_window)
        self.logger.log("Switched to window " + self.browser.title)

    def close(self):
        self.logger.log("END TEST")
        self.browser.close()