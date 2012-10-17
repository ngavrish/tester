from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from topface.model.custom_objects.auth import AuthForm
from topface.model.custom_objects.browser_window import BrowserWindow
from topface.model.model import Model

__author__ = 'ngavrish'

class XMLModel(Model):

    def __init__(self,browser,logger):
        self.browser = browser
        self.logger = logger
        self.window = BrowserWindow(self.browser, self.logger)

    def click(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        self.logger.log("Click Element = " + xpath)
        element = self.get_element_by_xpath(xpath)
        try:
            element.click()
        except Exception as e:
            print "Failed to simply click on element: " + e.message
            ActionChains(self.browser).move_to_element_with_offset(element, 1, 1).click().perform()

    def click_and_hold(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        raise NotImplementedError

    def click_at(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        raise NotImplementedError

    def click_at_and_hold(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        raise NotImplementedError

    def hover(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        element = self.get_element_by_xpath(xpath)
        self.logger.log("Hover element " + xpath)
        hover = ActionChains(self.browser).move_to_element(element)
        hover.perform()

    def enter_text(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        element = self.get_element_by_xpath(xpath)
        self.logger.log("Typing text = " + str(value) + " to element with xpath = " + xpath)
        element.clear()
        element.send_keys(value)

    def select_from_dropdown_by_index(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        dropdown = self.get_element_by_xpath(xpath)
        self.logger.log("Select element with index =  " + str(value))
        select = Select(dropdown)
        select.select_by_index(value)

    def select_from_dropdown_by_value(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        dropdown = self.get_element_by_xpath(xpath)
        self.logger.log("Select element with value = " + str(value))
        select = Select(dropdown)
        select.select_by_value(str(value))

    def select_from_dropdown_by_text(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        dropdown = self.get_element_by_xpath(xpath)
        self.logger.log("Select element with text = " + str(value))
        select = Select(dropdown)
        select.select_by_value(str(value))

    def get_selected_value_from_dropdown(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        dropdown = self.get_element_by_xpath(xpath)
        self.logger.log("Getting selected value from dropdown " + xpath)
        select = Select(dropdown)
        return select.first_selected_option.get_attribute("value")

    def authorize(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        auth = AuthForm(self.browser,self.logger)
        if platform == "fb-sa":
            if value == "User1":
                auth.login_with_fb_full_scale()

    def mark_user(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        pass

    def filter_city(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        pass

    def open_url(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        self.window.open(value)

    def switch_to_popup(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        self.window.switch_to_popup()

    def switch_to_root(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        self.window.switch_to_root()

    def logout(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        self.window.logout()

    def close(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        self.window.close()

    def assert_text(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        pass

    def assert_attribute(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        pass

    def assert_html(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        pass

    def assert_element(self,xpath=None,value=None,amount=None,time_delta=None,platform=None,coords=None):
        pass