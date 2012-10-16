from reports.logger import Logger
from topface import browser_mapping

__author__ = 'ngavrish'

class TestSuite:

    browser_name = "firefox"

    def __init__(self,name=None):
        if name is not None:
            try:
                self.set_browser_name(browser_mapping.browser_mapping[name])
                print "BROWSER = " + self.get_browser_name()
            except KeyError as e:
                raise KeyError("Test Suite's browser not found " + e.message)

    def set_browser_name(self,browser):
        TestSuite.browser_name = browser

    def get_browser_name(self):
        return TestSuite.browser_name