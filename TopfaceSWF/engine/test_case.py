from test_failed_exception import TestFailedException
from test_suite import TestSuite
from reports import logger
import settings
from selenium.webdriver import Firefox,Ie
from selenium.webdriver.support.wait import WebDriverWait


__author__ = 'user'


class TestCase(TestSuite):
    """
    pydoc

    """
    __log_name = ""
    __log_list = []

    def __init__(self):
        self.browser = None
        self.wait = None
        self.logger = None
        self.test_is_running = False


    def run_test(self):
        if TestSuite.browser_name == "firefox":
            self.browser = Firefox()
        elif TestSuite.browser_name == "ie":
            self.browser = Ie()
        self.wait = WebDriverWait(self.browser, settings.wait_for_element_time)
        self.logger = logger.Logger(self.get_log_name())
        self.logger.log(self.get_log_name()+"\r\n")

#        while not self.test_is_running:
#
        try:
            self.test_is_running = True
            self.run(self.browser)
            self.logger.log("\r\n<<<< SUCCESS >>>>\r\n")
        except TestFailedException as e:
            self.logger.log("\r\n ERROR: " + e.value + "\r\n<<<< TEST FAILED >>>>\r\n")
            self.browser.close()
        finally:
            self.test_is_running = False
            self.logger.dump_to_filesystem()
            self.set_log_list(self.logger.get_log_list())

    def run(self,browser):
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

    def set_log_name(self,name):
        self.__log_name = settings.get_topface_reports_path() + name + ".log"
