from engine.test_failed_exception import TestFailedException
import settings
from topface.model.marking import Marking
from topface.model.js_popups.fb_invite_popup import FbInviteFriendsPopup
from topface.model.model import Model

__author__ = 'user'

class AuthForm(Model):
    """

    """

    __social_switcher_id = "socialSwitcher"
    __social_list_xpath = "//div[@class='auth-form']//div[@class='social-list' and @style='display: block;']"
#    Facebook


    def __init__(self, browser, logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def click_social(self, social_name):
        try:
            self.click(
                self.get_element_by_id(self.__social_switcher_id)
            )
            self.wait4xpath(settings.wait_for_element_time, self.__social_list_xpath)
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

    def login_to_fb(self):
        try:
            password_input = self.wait4id(settings.wait_for_element_time, self.__FbAuth.password_input_id)
            login_input = self.wait4id(settings.wait_for_element_time, self.__FbAuth.login_input_id)

            password_input.clear()
            login_input.clear()

            login_input.send_keys(self.__FbAuth.login)
            password_input.send_keys(self.__FbAuth.password)

            self.click(
                self.get_element_by_id(self.__FbAuth.login_button_id)
            )
        except Exception as e:
            raise TestFailedException(e.message)

    def validate_fb_login_success(self):
        try:
            marking = Marking(self.browser,self.logger)
            fb_invite_popup = FbInviteFriendsPopup(self.browser,self.logger)

            marking.star_box()
            fb_invite_popup.close()
        except Exception as e:
            raise TestFailedException(e.message)

    def login_to_vk(self):
        try:
            password_input = self.wait4xpath(settings.wait_for_element_time, self.__VkAuth.password_input_xpath)
            login_input = self.wait4xpath(settings.wait_for_element_time, self.__VkAuth.login_input_xpath)

            password_input.clear()
            login_input.clear()

            login_input.send_keys(self.__VkAuth.login)
            password_input.send_keys(self.__VkAuth.password)

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
            marking = Marking(self.browser,self.logger)
            marking.star_box()
        except Exception as e:
            raise TestFailedException(e.message)

    class __FbAuth:
        option_id = "fb"
        login = "vpupkin-2012@mail.ru"
        password = "abc123123"
        login_input_id = "email"
        password_input_id = "pass"
        login_button_id = "loginbutton"

    class __VkAuth:
        option_id = "vk"
        login = "harare@yandex.ru"
        password = "cabzvilg"
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