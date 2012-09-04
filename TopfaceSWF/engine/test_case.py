from selenium.common.exceptions import NoSuchWindowException
from test_failed_exception import TestFailedException
from test_suite import TestSuite
from reports import logger
import settings
from selenium.webdriver import Firefox,Ie
from selenium.webdriver.support.wait import WebDriverWait


__author__ = 'ngavrish'


class TestCase(TestSuite):
    """
    pydoc

    """
    __log_name = ""
    __log_path = ""
    __screen_path = ""
    __log_list = []

    #noinspection PyMissingConstructor
    def __init__(self):
        self.browser = None
        self.wait = None
        self.logger = None
        self.test_is_running = False

    #noinspection PyArgumentList
    def run_test(self):
        """

        """
        if TestSuite.browser_name == "firefox":
            self.browser = Firefox()
        elif TestSuite.browser_name == "ie":
            self.browser = Ie()
        self.logger = logger.Logger(self.get_log_path())
        self.logger.log(self.get_log_name()+"\r\n")

#        while not self.test_is_running:

        try:
            self.test_is_running = True
#            Method is overridden in child object
            self.run(self.browser,self.logger)
            self.logger.log("\r\n<<<< SUCCESS >>>>\r\n")
        except TestFailedException as e:
            self.browser.get_screenshot_as_file(self.get_screen_path())
            self.logger.log("\r\n ERROR: " + e.value + "\r\n<<<< TEST FAILED >>>>\r\n")
            try:
                self.browser.close()
            except NoSuchWindowException as e:
                print "ERROR: Cannot close window after Test Failed: " + e.message
                self.logger.log("ERROR: Cannot close window after Test Failed: " + e.message)
        finally:
            self.test_is_running = False
            self.logger.dump_to_filesystem()
            self.set_log_list(self.logger.get_logs())

    def run(self):
         pass

    def get_browser(self):
        pass
#   dump test case results to file system
#    return TestCase log

    def set_log_list(self,logs):
        self.__log_list = logs

    def get_log_list(self):
        return self.__log_list

    def get_log_name(self):
        return self.__log_name

    def get_log_path(self):
        return self.__log_path

    def get_screen_path(self):
        return self.__screen_path

    def set_log_name(self,name):
        self.__log_path = settings.get_topface_reports_path() + name + ".log"
        self.__log_name = name
        self.__screen_path = settings.get_topface_reports_path() + name + ".png"
