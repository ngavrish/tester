import traceback
from selenium.common.exceptions import NoSuchWindowException
import time
from dao.dao import DataAccessObject
from test_failed_exception import TestFailedException
from test_suite import TestSuite
from reports import logger
import settings
from selenium.webdriver import Firefox,Ie
from selenium.webdriver.support.wait import WebDriverWait
from topface import profiling_events


__author__ = 'ngavrish'

def timer(f):
    def func(*args, **kwargs):
        currtime = time.time()
        f(*args, **kwargs)
        s = time.time()-currtime
        TestCase().logger.log(" ====== Time running function " + f.__name__ + " = " + str(s) + " ========= ")
        return s
    return func

class TestCase(TestSuite):
    """
    pydoc

    """
    __log_name = ""
    __log_path = ""
    __screen_path = ""

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
#        print "Browser  name = " + TestSuite().get_browser_name()
        if TestSuite.browser_name == "firefox":
            self.browser = Firefox()
        elif TestSuite.browser_name == "ie":
            self.browser = Ie()
        self.logger = logger.Logger(self.get_log_path())
        self.logger.log_name = self.get_log_name()
        self.logger.log("====================\r\n")
        self.logger.log(self.get_log_name()+"\r\n")
        self.logger.log("====================\r\n")
#        IF true => test succeeded, else => test failed
        status = True
#        while not self.test_is_running:
        try:
            self.test_is_running = True
#            Method is overridden in child object
            self.run(self.browser,self.logger)
            self.logger.log("\r\n<<<< SUCCESS >>>>\r\n")
        except TestFailedException as e:
            status = False
            self.browser.get_screenshot_as_file(self.get_screen_path())
            self.logger.log("\r\n ERROR: " + e.value + "\r\n Stacktrace: "
                            + traceback.format_exc() + "<<<< TEST FAILED >>>>\r\n")
            try:
                self.browser.close()
            except NoSuchWindowException as e:
                print "ERROR: Cannot close window after Test Failed: " + e.message
                self.logger.log("ERROR: Cannot close window after Test Failed: " + e.message)
        finally:
            self.test_is_running = False
            self.logger.dump_to_filesystem()
            return {self.logger.log_name:[self.logger.get_logs(),status]}

    def run(self):
         pass

    def get_browser(self):
        pass
#   dump test case results to file system
#    return TestCase log

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

    def do_method(self,method,element_type=None,*args):
        dao = DataAccessObject()
        t0 = time.time()
        self.logger.log("TIME0 = " + str(t0))
        method(*args)
        result_time = time.time() - t0
        self.logger.log("EXECUTION TIME = " + str(result_time) + " seconds")
        try:
            if element_type == profiling_events.login_event:
                self.logger.log("INSERT INTO LOGIN_TIMELINE_TABLE")
                dao.insert_into_login_timeline_table(result_time)

            elif element_type == profiling_events.message_sent_event:
                self.logger.log("INSERT INTO PROFILE_EVENTS_TABLE")
                dao.insert_into_send_message_timeline_table(result_time)

            elif element_type == profiling_events.questionary_edited_event:
                self.logger.log("INSERT INTO QUESTIONARY_TIMELINE_TABLE")
                dao.insert_into_questionary_timeline_table(result_time)

            elif element_type == profiling_events.user_marked_event:
                self.logger.log("INSERT INTO MARKS_TIMELINE_TABLE")
                dao.insert_into_mark_user_timeline_table(result_time)

            elif element_type == profiling_events.user_navigated_event:
                self.logger.log("INSERT INTO NAVIGATION_TIMELINE_TABLE")
                dao.insert_into_user_navigation_timeline_table(result_time)

        except TestFailedException as e:
            raise TestFailedException("Failed to put in log time metrics " + e.message)