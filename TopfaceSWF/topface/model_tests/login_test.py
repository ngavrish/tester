from engine.test_failed_exception import TestFailedException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from engine.test_case import TestCase
from engine.test_suite import TestSuite

__author__ = 'user'

class LoginTestSuite(TestSuite):

    def run(self):
        test_cases = [self.LoginFacebookSuccess("LoginFacebookSuccessTest"),
                    self.LoginVkSuccess("LoginVkontakteSuccessTest"),
                    self.LoginMailruSuccess("LoginMailruSuccessTest")]
        for test_case in test_cases:
            test_case.run_test()


    class LoginFacebookSuccess(TestCase):

        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self, browser):
            # Get local session of firefox
            browser.get("http://topface.com") # Load page
            assert browser.current_url == "http://topface.com/ru/auth/?url=%2F"
            browser.find_element_by_id("socialSwitcher").click()

#            raise TestFailedException("Debug Exception")
            try:
                element = WebDriverWait(browser, 100).until(lambda driver: driver.find_element_by_xpath(
                    "//div[@class='auth-form']//div[@class='social-list' and @style='display: block;']"))
                #
                # For Chrome
                # element = WebDriverWait(browser, 100).until(lambda driver : driver.find_element_by_xpath("//*[@id='mainLayout']/div[2]/div[1]/div[1]/div[2]"))
            except NoSuchElementException:
                print "Failed to wait for element"
            browser.find_element_by_id("fb").click()
            parent_h = browser.current_window_handle
            # click on the link that opens a new window
            handles = browser.window_handles
            # before the pop-up window closes
            handles.remove(parent_h)
            browser.switch_to_window(handles.pop())
            try:
                fb_password = WebDriverWait(browser, 100).until(lambda driver: driver.find_element_by_id("pass"))
                fb_email = WebDriverWait(browser, 100).until(lambda driver: driver.find_element_by_id("email"))

                fb_email.clear()
                fb_password.clear()

                fb_email.send_keys("nikikikita@mail.ru")
                fb_password.send_keys("cabzvilg")
            except NoSuchElementException:
                print "Failed to wait for element"
                # do stuff in the popup
            # popup window closes
            browser.find_element_by_id('loginbutton').click()
            browser.switch_to_window(parent_h)
            try:
                WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_id("starBox"))
            except Exception:
                print "Failed to wait for element"
            try:
                fb_close = WebDriverWait(browser, 10).until(
                    lambda driver: driver.find_element_by_xpath("//div[@id='fb-root']/div[2]/a"))
                fb_close.click()
            except NoSuchElementException:
                pass
            except TimeoutException:
                print "Facebook invite window didn't open"
            browser.close()

    class LoginVkSuccess(TestCase):

        def __init__(self,test_name):
            self.set_log_name(test_name)

    # Get local session of firefox
        def run(self,browser):
            browser.get("http://topface.com") # Load page
            assert browser.current_url == "http://topface.com/ru/auth/?url=%2F"
            browser.find_element_by_id("socialSwitcher").click()

            try:
                element = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_xpath(
                    "//div[@class='auth-form']//div[@class='social-list' and @style='display: block;']"))
                #
                # For Chrome
                # element = WebDriverWait(browser, 100).until(lambda driver : driver.find_element_by_xpath("//*[@id='mainLayout']/div[2]/div[1]/div[1]/div[2]"))
            except NoSuchElementException:
                print "Failed to wait for element"
            browser.find_element_by_id("vk").click()
            parent_h = browser.current_window_handle
            # click on the link that opens a new window
            handles = browser.window_handles
            # before the pop-up window closes
            handles.remove(parent_h)
            browser.switch_to_window(handles.pop())
            try:
                vk_password = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_xpath("//div[@id='box']//table[@class='login']//input[@name='pass']"))
                vk_email = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_xpath("//div[@id='box']//table[@class='login']//input[@name='email']"))

                vk_email.clear()
                vk_password.clear()
                vk_email.send_keys("harare@yandex.ru")
                vk_password.send_keys("cabzvilg")
            except TimeoutException:
                raise TimeoutException("Failed to wait for element")
                # do stuff in the popup
            # system login
            browser.find_element_by_id('install_allow').click()
            # get back to parent window
            browser.switch_to_window(parent_h)
            try:
                WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_id("starBox"))
            except TimeoutException:
                raise TimeoutException("Failed to wait for element")
            browser.close()

    class LoginMailruSuccess(TestCase):

        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self,browser):
            # Get local session of firefox
            browser.get("http://topface.com") # Load page
            try:
                assert browser.current_url == "http://topface.com/ru/auth/?url=%2F"
            except AssertionError:
                raise TestFailedException("Wrong url.  http://topface.com/ru/auth/?url=%2F != " + browser.current_url)
            browser.find_element_by_id("socialSwitcher").click()

            try:
                element = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_xpath(
                    "//div[@class='auth-form']//div[@class='social-list' and @style='display: block;']"))
                #
                # For Chrome
                # element = WebDriverWait(browser, 100).until(lambda driver : driver.find_element_by_xpath("//*[@id='mainLayout']/div[2]/div[1]/div[1]/div[2]"))
            except NoSuchElementException:
                raise NoSuchElementException("Failed to wait for element")
            browser.find_element_by_id("mm").click()
            parent_h = browser.current_window_handle
            # click on the link that opens a new window
            handles = browser.window_handles
            # before the pop-up window closes
            handles.remove(parent_h)
            browser.switch_to_window(handles.pop())
            try:
                mailru_email = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_xpath("//div[@id='content']//input[@name='Login']"))
                mailru_pass = WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_xpath("//div[@id='content']//input[@name='Password']"))

                mailru_email.clear()
                mailru_pass.clear()
                mailru_email.send_keys("vpupkin-2012")
                mailru_pass.send_keys("abc123123")
            except TimeoutException:
                raise TimeoutException("Failed to wait for element")
                # do stuff in the popup
            # system login
            browser.find_element_by_xpath("//div[@class='highlight tar']//button").click()
            # get back to parent window
            browser.switch_to_window(parent_h)
            try:
                WebDriverWait(browser, 10).until(lambda driver: driver.find_element_by_id("starBox"))
            except TimeoutException:
                raise TimeoutException("Failed to wait for element")
            browser.close()