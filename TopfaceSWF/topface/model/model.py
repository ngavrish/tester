from abc import abstractmethod, ABCMeta, abstractproperty
from engine.test_failed_exception import TestFailedException
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import settings

__author__ = 'ngavrish'

class Model:

    __metaclass__=ABCMeta

    def __init__(self,browser,logger):
        self.logger = logger
        self.browser = browser

    def get_element_by_xpath(self,xpath):
        self.logger.log("Find element by XPATH = " + xpath)
        try:
            return WebDriverWait(self.browser, settings.wait_for_element_time).\
            until(lambda driver: driver.find_element_by_xpath(xpath))
        except Exception:
            raise TestFailedException("Failed to get element by xpath = " + xpath)

    def get_element_by_id(self,id):
        self.logger.log("Find element by ID = " + id)
        return self.browser.find_element_by_id(id)

    @abstractmethod
    def click(self,element):
        raise NotImplementedError

    @abstractmethod
    def click_and_hold(self,element):
        raise NotImplementedError

    @abstractmethod
    def click_at(self,element,coords):
        raise NotImplementedError

    @abstractmethod
    def click_at_and_hold(self,element,coords):
        raise NotImplementedError

    @abstractmethod
    def hover(self,element):
        raise NotImplementedError

    @abstractmethod
    def enter_text(self,element,text):
        raise NotImplementedError

    @abstractmethod
    def select_from_dropdown_by_index(self,dropdown,element_index):
        raise NotImplementedError

    @abstractmethod
    def select_from_dropdown_by_value(self,dropdown,value):
        raise NotImplementedError

    @abstractmethod
    def select_from_dropdown_by_text(self,dropdown,value):
        raise NotImplementedError

    @abstractmethod
    def get_selected_value_from_dropdown(self,dropdown):
        raise NotImplementedError
