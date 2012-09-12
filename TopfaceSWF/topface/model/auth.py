# coding=utf-8
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.js_popups.dreams_popup import DreamsPopup
from topface.model.marks import Marks
from topface.model.browser_window import BrowserWindow
from topface.model.js_popups.fb_invite_popup import FbInviteFriendsPopup
from topface.model.model import Model
from topface.model.js_popups.sexy_popup import SexyPopup

__author__ = 'ngavrish'

class AuthForm(Model):
    """

    """

    _social_switcher_id = "socialSwitcher"
    _social_list_xpath = "//div[@class='auth-form']//div[@class='social-list' and @style='display: block;']"
#    Facebook

    def __init__(self, browser, logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def click_social(self, social_name):
        try:
            self.click(
                self.get_element_by_id(self._social_switcher_id)
            )
            self.wait4xpath(settings.wait_for_element_time, self._social_list_xpath)
            if social_name == "facebook":
                self.click(
                    self.get_element_by_id(self.__FbAuth.option_id)
                )
            elif social_name == "vkontakte":
                self.click(
                    self.get_element_by_id(self.__VkAuth.option_id)
                )
            elif social_name == "mail.ru":
                self.click(
                    self.get_element_by_id(self.__MailruAuth.option_id)
                )

        except Exception as e:
            raise TestFailedException(e.message)
        # For Chrome
        # element = WebDriverWait(browser, 100).until(lambda driver : driver.find_element_by_xpath("//*[@id='mainLayout']/div[2]/div[1]/div[1]/div[2]"))

    def login_to_fb(self,user=None):
        if user is None:
            user = self.User1
        try:
            password_input = self.wait4id(settings.wait_for_element_time, self.__FbAuth.password_input_id)
            login_input = self.wait4id(settings.wait_for_element_time, self.__FbAuth.login_input_id)

            password_input.clear()
            login_input.clear()

            login_input.send_keys(user.login)
            password_input.send_keys(user.password)

            self.click(
                self.get_element_by_id(self.__FbAuth.login_button_id)
            )
        except Exception as e:
            raise TestFailedException(e.message)

    def validate_fb_login_success(self):
        try:
            marks = Marks(self.browser,self.logger)
            fb_invite_popup = FbInviteFriendsPopup(self.browser,self.logger)
            sexy_popup = SexyPopup(self.browser,self.logger)


            marks.star_box()
            fb_invite_popup.close()
            sexy_popup.close()
        except Exception as e:
            raise TestFailedException(e.message)

    def login_to_vk(self,user=None):
        if user is None:
            user = self.User1

        try:
            password_input = self.wait4xpath(settings.wait_for_element_time, self.__VkAuth.password_input_xpath)
            login_input = self.wait4xpath(settings.wait_for_element_time, self.__VkAuth.login_input_xpath)

            password_input.clear()
            login_input.clear()

            login_input.send_keys(user.login)
            password_input.send_keys(user.password)

            self.click(
                self.get_element_by_id(self.__VkAuth.login_button_id)
            )
        except Exception as e:
            raise TestFailedException(e.message)

    def login_to_mailru(self):
        try:
            password_input = self.wait4xpath(settings.wait_for_element_time, self.__MailruAuth.password_input_xpath)
            login_input = self.wait4xpath(settings.wait_for_element_time, self.__MailruAuth.login_input_xpath)

            password_input.clear()
            login_input.clear()

            login_input.send_keys(self.__MailruAuth.login)
            password_input.send_keys(self.__MailruAuth.password)

            self.click(
                self.get_element_by_xpath(self.__MailruAuth.login_button_xpath)
            )
        except Exception as e:
            raise TestFailedException(e.message)

    def validate_login_success(self):
        try:
            marks = Marks(self.browser,self.logger)
            dreams_popup = DreamsPopup(self.browser,self.logger)

            marks.star_box()
            dreams_popup.close()
        except Exception as e:
            raise TestFailedException(e.message)

    def login_with_fb_full_scale(self, user=None):
        if user is None:
            user = self.User1

        window = BrowserWindow(self.browser, self.logger)

        window.open(settings.target_url)
        try:
            assert window.get_current_url() == window.get_unauthorised_url()
        except AssertionError:
            raise TestFailedException("Wrong URL")

        self.click_social("facebook")
        window.switch_to_popup()
        self.login_to_fb(user)
        window.switch_to_root()
        self.validate_fb_login_success()

    def login_with_vk_full_scale(self, user=None):
        if user is None:
            user = self.User1

        window = BrowserWindow(self.browser, self.logger)

        window.open(settings.target_url)
        try:
            assert window.get_current_url() == window.get_unauthorised_url()
        except AssertionError:
            raise TestFailedException("Wrong URL")

        self.click_social("vkontakte")
        window.switch_to_popup()
        self.login_to_vk(user)
        window.switch_to_root()
        self.validate_login_success()

    class User1:
        login = "vpupkin-89@mail.ru"
        password = "abc123123"
        profile_url = "http://topface.com/profile/41694213/"
        fb_human_name = "Vasya"
        fb_human_age = "92"
        fb_human_place = u"Москва, Россия"

    class User2:
        login = "vpupkin-89@inbox.ru"
        password = "abc123123"
        profile_url = "http://topface.com/profile/41717695/"

#        Research users:
    class MSK_24_Male:
        login = "vpupkin-89@inbox.ru"
        password = "abc123123"
        profile_url = "http://topface.com/profile/41803067/"

    class MSK_20_Female:
        login = "vpupkin-89@mail.ru"
        password = "abc123123"
        profile_url = "http://topface.com/profile/41804454/"

    class __FbAuth:
        option_id = "fb"
        login_input_id = "email"
        password_input_id = "pass"
        login_button_id = "loginbutton"

    class __VkAuth:
        option_id = "vk"
        login_input_xpath = "//div[@id='box']//table[@class='login']//input[@name='email']"
        password_input_xpath = "//div[@id='box']//table[@class='login']//input[@name='pass']"
        login_button_id = "install_allow"

    class __MailruAuth:
        option_id = "mm"
        login = "vpupkin-2012"
        password = "abc123123"
        login_input_xpath = "//div[@id='content']//input[@name='Login']"
        password_input_xpath = "//div[@id='content']//input[@name='Password']"
        login_button_xpath = "//div[@class='highlight tar']//button"