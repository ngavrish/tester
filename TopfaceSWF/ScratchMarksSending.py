#!/usr/bin/python
# -*- coding: utf8 -*-

from webbrowser import browser
from selenium.webdriver.support.wait import WebDriverWait

__author__ = 'user'

import sys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import selenium.webdriver.support.ui as ui
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
import time


class VkontakteMarksSending:
    def __init__(self):
        reload(sys)
        sys.setdefaultencoding("utf-8")
        self.browser = webdriver.Firefox()
        self.wait = WebDriverWait(self.browser, 10)

    def login_fb_success(self):
    # Get local session of firefox
        self.browser.get("http://topface.com") # Load page
        assert self.browser.current_url == "http://topface.com/ru/auth/?url=%2F"
        self.browser.find_element_by_id("socialSwitcher").click()

        try:
            element = WebDriverWait(self.browser, 100).until(lambda driver: driver.find_element_by_xpath(
                "//div[@class='auth-form']//div[@class='social-list' and @style='display: block;']"))
            #
            # For Chrome
            # element = WebDriverWait(self.browser, 100).until(lambda driver : driver.find_element_by_xpath("//*[@id='mainLayout']/div[2]/div[1]/div[1]/div[2]"))
        except NoSuchElementException:
            print "Failed to wait for element"
        self.browser.find_element_by_id("fb").click()
        parent_h = self.browser.current_window_handle
        # click on the link that opens a new window
        handles = self.browser.window_handles
        # before the pop-up window closes
        handles.remove(parent_h)
        self.browser.switch_to_window(handles.pop())
        try:
            fb_password = WebDriverWait(self.browser, 100).until(lambda driver: driver.find_element_by_id("pass"))
            fb_email = WebDriverWait(self.browser, 100).until(lambda driver: driver.find_element_by_id("email"))

            fb_email.clear()
            fb_password.clear()

            fb_email.send_keys("nikikikita@mail.ru")
            fb_password.send_keys("cabzvilg")
        except NoSuchElementException:
            print "Failed to wait for element"
            # do stuff in the popup
        # popup window closes
        self.browser.find_element_by_id('loginbutton').click()
        self.browser.switch_to_window(parent_h)
        try:
            WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_id("starBox"))
        except Exception:
            print "Failed to wait for element"
        try:
            fb_close = WebDriverWait(self.browser, 10).until(
                lambda driver: driver.find_element_by_xpath("//div[@id='fb-root']/div[2]/a"))
            fb_close.click()
        except NoSuchElementException:
            pass
        except TimeoutException:
            print "Facebook invite window didn't open"
        self.browser.close()


    def login_vk_success(self):
    # Get local session of firefox
        self.browser.get("http://topface.com") # Load page
        assert self.browser.current_url == "http://topface.com/ru/auth/?url=%2F"
        self.browser.find_element_by_id("socialSwitcher").click()

        try:
            element = WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_xpath(
                "//div[@class='auth-form']//div[@class='social-list' and @style='display: block;']"))
            #
            # For Chrome
            # element = WebDriverWait(self.browser, 100).until(lambda driver : driver.find_element_by_xpath("//*[@id='mainLayout']/div[2]/div[1]/div[1]/div[2]"))
        except NoSuchElementException:
            print "Failed to wait for element"
        self.browser.find_element_by_id("vk").click()
        parent_h = self.browser.current_window_handle
        # click on the link that opens a new window
        handles = self.browser.window_handles
        # before the pop-up window closes
        handles.remove(parent_h)
        self.browser.switch_to_window(handles.pop())
        try:
            vk_password = WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_xpath("//div[@id='box']//table[@class='login']//input[@name='pass']"))
            vk_email = WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_xpath("//div[@id='box']//table[@class='login']//input[@name='email']"))

            vk_email.clear()
            vk_password.clear()
            vk_email.send_keys("harare@yandex.ru")
            vk_password.send_keys("cabzvilg")
        except TimeoutException:
            raise TimeoutException("Failed to wait for element")
            # do stuff in the popup
        # system login
        self.browser.find_element_by_id('install_allow').click()
        # get back to parent window
        self.browser.switch_to_window(parent_h)
        try:
            WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_id("starBox"))
        except TimeoutException:
            raise TimeoutException("Failed to wait for element")
        self.browser.close()

    def login_mailru_success(self):
    # Get local session of firefox
        self.browser.get("http://topface.com") # Load page
        assert self.browser.current_url == "http://topface.com/ru/auth/?url=%2F"
        self.browser.find_element_by_id("socialSwitcher").click()

        try:
            element = WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_xpath(
                "//div[@class='auth-form']//div[@class='social-list' and @style='display: block;']"))
            #
            # For Chrome
            # element = WebDriverWait(self.browser, 100).until(lambda driver : driver.find_element_by_xpath("//*[@id='mainLayout']/div[2]/div[1]/div[1]/div[2]"))
        except NoSuchElementException:
            raise NoSuchElementException("Failed to wait for element")
        self.browser.find_element_by_id("mm").click()
        parent_h = self.browser.current_window_handle
        # click on the link that opens a new window
        handles = self.browser.window_handles
        # before the pop-up window closes
        handles.remove(parent_h)
        self.browser.switch_to_window(handles.pop())
        try:
            mailru_email = WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_xpath("//div[@id='content']//input[@name='Login']"))
            mailru_pass = WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_xpath("//div[@id='content']//input[@name='Password']"))

            mailru_email.clear()
            mailru_pass.clear()
            mailru_email.send_keys("vpupkin-2012")
            mailru_pass.send_keys("abc123123")
        except TimeoutException:
            raise TimeoutException("Failed to wait for element")
            # do stuff in the popup
        # system login
        self.browser.find_element_by_xpath("//div[@class='highlight tar']//button").click()
        # get back to parent window
        self.browser.switch_to_window(parent_h)
        try:
            WebDriverWait(self.browser, 10).until(lambda driver: driver.find_element_by_id("starBox"))
        except TimeoutException:
            raise TimeoutException("Failed to wait for element")
        self.browser.close()
        #        self.browser.close()

        #    def mark_user_one2eight(self):
        #
        #        marks_list = self.browser.find_elements_by_xpath(".//*[@id='starBox']//a[@data-index!='0' and @data-index!='9' and @data-index!='10']")
        #        for mark in marks_list:
        #            profileLink1 = self.browser.find_element_by_xpath("//div[@id='userPhotoLayout']/a").get_attribute("href")
        #            hover = ActionChains(self.browser).move_to_element(mark)
        #            hover.perform()
        #            try:
        #                mark.click()
        #            except ElementNotVisibleException:
        #                print "Element = " + mark.get_attribute("innerHTML") + " element "
        #            profileLink2 = self.browser.find_element_by_xpath("//div[@id='userPhotoLayout']/a").get_attribute("href")
        #
        #            assert profileLink1 != profileLink2
        #            print mark
        #
        #        self.browser.find_element_by_id("exit").click()
        ##        self.browser.close()
        #
        #    def mark_user_top_user_message(self):
        #        marks_list = self.browser.find_elements_by_xpath(".//*[@id='starBox']//a[@data-index='9' or @data-index='10']")
        #        for mark in marks_list:
        #            profileLink1 = self.browser.find_element_by_xpath("//div[@id='userPhotoLayout']/a").get_attribute("href")
        #            hover = ActionChains(self.browser).move_to_element(mark)
        #            hover.perform()
        #            try:
        #                self.browser.implicitly_wait(5)
        #                mark.click()
        #                try:
        #                    high_rate_comment = WebDriverWait(self.browser, 5).until(lambda driver :
        #                                        driver.find_element_by_xpath(".//*[@id='extraQuestions']//div[@class='questions-list']/textarea"))
        #                    assert u'Свой вариант' == high_rate_comment.get_attribute("placeholder")
        #
        #                    if high_rate_comment.get_attribute("style") == "":
        #                        print "style = " + high_rate_comment.get_attribute("style")
        #                    else:
        #                        print "Style of the element exists, but it shouldn't"
        #                        raise Exception("Style of the element exists, but it shouldn't")
        #
        #                    high_rate_comment.click()
        #                    try:
        #                        WebDriverWait(self.browser, 5).until(
        #                            lambda driver :
        #                                driver
        #                                    .find_element_by_xpath(".//*[@id='extraQuestions']//div[@class='questions-list']/textarea")
        #                                    .get_attribute("style")
        #                                    .count("35px") > 0)
        #                    except Exception:
        #                        print "Textarea expanding didn't happen"
        #
        ##                    Validate that message contains more that 1 symbol
        #                    high_rate_comment.send_keys(u"1")
        #                    self.browser.find_element_by_id('btnSendExtra').click()
        #                    try:
        #                        validate_alert_form_ok = WebDriverWait(self.browser, 5).until(lambda driver : driver.find_element_by_xpath(".//div[text()='Ваше сообщение слишком короткое, напишите более развернуто.']//a"))
        #                        validate_alert_form_ok.click()
        #                    except NoSuchElementException:
        #                        print "Element not found. Too short message alert"
        ##                   End validation
        #                    high_rate_comment.send_keys(u"Привет")
        #                    self.browser.find_element_by_id('btnSendExtra').click()
        #                except NoSuchElementException:
        #                    pass
        #                except TimeoutException:
        #                    print "Textarea not found"
        #            except ElementNotVisibleException:
        #                print "Element NOT visible = " + mark.get_attribute("innerHTML")
        #            profileLink2 = self.browser.find_element_by_xpath("//div[@id='userPhotoLayout']/a").get_attribute("href")
        #            print "Element = " + mark.get_attribute("innerHTML")
        #            print profileLink1
        #            print profileLink2
        #
        #            assert profileLink1 != profileLink2
        #
        #        self.browser.find_element_by_id("exit").click()
        #        self.browser.close()

#    def mark_user_top_standart_messages(self):
#        marks_list = self.browser.find_elements_by_xpath(".//*[@id='starBox']//a[@data-index='9' or @data-index='10']")
#        for mark in marks_list:
#            profileLink1 = self.browser.find_element_by_xpath("//div[@id='userPhotoLayout']/a").get_attribute("href")
#            hover = ActionChains(self.browser).move_to_element(mark).click()
#            hover.perform()
#            try:
#                high_rate_comment = WebDriverWait(self.browser, 5).until(lambda driver:
#                driver.find_element_by_xpath(".//*[@id='extraQuestions']//div[@class='questions-list']/textarea"))
#                assert u'Свой вариант' == high_rate_comment.get_attribute("placeholder")
#                print high_rate_comment.get_attribute("placeholder")
#
#                if high_rate_comment.get_attribute("style") != "":
#                    print "style = " + high_rate_comment.get_attribute("style")
#                    raise Exception("Style of the element exists, but it shouldn't")
#
#                try:
#                    random_compliments =\
#                    WebDriverWait(self.browser, 5).\
#                    until(lambda driver:
#                    driver.find_elements_by_xpath(
#                        ".//*[@id='extraQuestions']//div[@class='questions-list']//label[contains(@class,'message-variant random-compliments')]"))
#                except TimeoutException:
#                    raise TimeoutException("Compliments box not found")
#
#                for compliment in random_compliments:
#                    initial_textarea_value = self.browser.execute_script(
#                        "return $(\"textarea[class='extra-rate-comment-area not-empty']\").val()")
#                    ActionChains(self.browser).move_to_element(high_rate_comment).click()
#                    self.browser.implicitly_wait(2)
#                    compliment.click()
#                    self.browser.implicitly_wait(2)
#                    print compliment.get_attribute("innerHTML")
#                    # debug output //
#                    try:
#                        WebDriverWait(self.browser, 5).until(
#                            lambda driver:
#                            driver
#                            .find_element_by_xpath(".//*[@id='extraQuestions']//div[@class='questions-list']/textarea")
#                            .get_attribute("style")
#                            .count("35px") > 0)
#                    except Exception:
#                        raise Exception("Textarea expanding didn't happen")
#                        # validate that textarea text has changed
#                    print initial_textarea_value
#                    print self.browser.execute_script(
#                        "return $(\"textarea[class='extra-rate-comment-area not-empty']\").val()")
#                    assert initial_textarea_value !=\
#                           self.browser.execute_script(
#                               "return $(\"textarea[class='extra-rate-comment-area not-empty']\").val()")
#            except NoSuchElementException:
#                pass
#            except TimeoutException:
#                print "Textarea not found"
#            self.browser.find_element_by_id('btnSendExtra').click()
#
#        profileLink2 = self.browser.find_element_by_xpath("//div[@id='userPhotoLayout']/a").get_attribute("href")
#        print "Element = " + mark.get_attribute("innerHTML")
#
#        assert profileLink1 != profileLink2
#
#        self.browser.find_element_by_id("exit").click()
#        self.browser.close()

#    def mark_energy_charge_test(self):
#        percent_energy = float(self.browser\
#            .find_element_by_xpath(".//*[@id='sideMenu']//div[contains(@class,'val')]")\
#            .get_attribute("innerHTML")[:-1]\
#            .replace(",","."))
#        marks_left_till_plus = self.browser.\
#        find_element_by_xpath("//div[@id='user-rates-bonus-block']//span[@class='power-bonus-message']").get_attribute("innerHTML")
#        marks_left = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
#
#        mark_five = self.browser.find_element_by_xpath(".//*[@id='starBox']//a[@data-index='5']")
#
#        for i in range(marks_left):
#            marks_left_till_plus = self.browser.\
#                find_element_by_xpath("//div[@id='user-rates-bonus-block']//span[@class='power-bonus-message']").get_attribute("innerHTML")
#            marks_left_new_before_click = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
#            hover = ActionChains(self.browser).move_to_element(mark_five)
#            hover.perform()
#            mark_five.click()
#            print i
#            marks_left_till_plus = self.browser.\
#                find_element_by_xpath("//div[@id='user-rates-bonus-block']//span[@class='power-bonus-message']").get_attribute("innerHTML")
#            marks_left_new_after_click = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
#            assert marks_left_new_after_click == (marks_left_new_before_click - 1)
#        assert percent_energy == float(self.browser\
#                                       .find_element_by_xpath(".//*[@id='sideMenu']//div[contains(@class,'val')]")\
#                                       .get_attribute("innerHTML")[:-1]\
#                                        .replace(",",".")) + 3
#        self.browser.close()
#
#    def mark_vk_accuracy(self):
#        # firebug Crash. Cannot implement VK-specific automation tests
#        pass
#
#    def run(self):
#        browser = webdriver.Firefox() # Get local session of firefox
#        browser.get("http://topface.com") # Load page
#        assert browser.current_url == "http://topface.com/ru/auth/?url=%2F"
#        socSwitcher = browser.find_element_by_id("socialSwitcher")
#        socSwitcher.click()
#        browser.close()

test = VkontakteMarksSending()
#test.login_fb_success()
test.login_mailru_success()
test.login_fb_success()
test.login_vk_success()
#test.mark_vk_accuracy()