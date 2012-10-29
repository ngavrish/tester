import traceback
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from engine.test_failed_exception import TestFailedException
import time
import settings
from topface.model.model import Model

__author__ = 'ngavrish'


class ObjectModel(Model):

    def __init__(self, browser, logger):
        super(ObjectModel, self).__init__(browser, logger)

    def get_element_xpath(self, element):
        self.logger.log("Getting element = " + str(element) + "xpath ")
        return self.browser.\
                execute_script(
                                "gPt=function(c){if(c.id!==''){return'id(\"'+c.id+'\")'}if(c===document.body){return c.tagName}var a=0;var e=c.parentNode.childNodes;for(var b=0;b<e.length;b++){var d=e[b];if(d===c){return gPt(c.parentNode)+'/'+c.tagName+'['+(a+1)+']'}if(d.nodeType===1&&d.tagName===c.tagName){a++}}};return gPt(arguments[0]).toLowerCase();",element)

    def click(self, element):
        self.logger.log("Click Element = " + self.get_element_xpath(element))
        try:
            element.click()
        except Exception as e:
            print "Failed to simply click on element: " + e.message
            ActionChains(self.browser).move_to_element_with_offset(element, 1, 1).click().perform()
#            sleep(2)

    def click_and_hold(self,element):
        pass

    def click_at(self,element,coords):
        pass

    def click_at_and_hold(self,element,coords):
        pass

    def hover(self,element):
        self.logger.log("Hover element " + self.get_element_xpath(element))
        hover = ActionChains(self.browser).move_to_element(element)
        hover.perform()

    def drag_and_drop(self,element,offsetx,offsety):
        self.logger.log("Dragging element " + self.get_element_xpath(element) + " with offset x = " +
                        str(offsetx) + " with offset y " + str(offsety))
        dragandrop = ActionChains(self.browser).drag_and_drop_by_offset(element,offsetx,offsety)
        dragandrop.perform()

    def key_down(self):
        pass

    def enter_text(self,element,text):
        self.logger.log("Typing text = " + str(text) + " to element with xpath = " +
                        self.get_element_xpath(element))
        element.clear()
        element.send_keys(text)

    def select_from_dropdown_by_index(self,dropdown,element_index):
        self.logger.log("Select element with index =  " + str(element_index))
        select = Select(dropdown)
        select.select_by_index(element_index)

    def select_from_dropdown_by_value(self,dropdown,value):
        self.logger.log("Select element with value = " + str(value))
        select = Select(dropdown)
        self.logger.log("Dropdown was found")
        try:
            select.select_by_value(str(value))
        except Exception as e:
            print
            raise TestFailedException("Failed to select value = " + str(value) + " from selectbox " + traceback.format_exc())
        self.logger.log("Value = " + str(value) + " was selected")

    def select_from_invisible_dropdown_by_value(self,drop_down_xpath,value):
        self.logger.log("Selecting from invisible dropdown with xpath = " + drop_down_xpath)
        self.click(
            self.get_element_by_xpath())

    def select_from_dropdown_by_text(self,dropdown,value):
        self.logger.log("Select element with text = " + str(value))
        select = Select(dropdown)
        select.select_by_value(str(value))

    def get_selected_value_from_dropdown(self,dropdown):
        self.logger.log("Getting selected value from dropdown " + self.get_element_xpath(dropdown))
        select = Select(dropdown)
        return select.first_selected_option.get_attribute("value")

    def wait4xpath(self,time,xpath):
        self.logger.log("Waiting for element XPATH = " + xpath)
        return WebDriverWait(self.browser, time).until(lambda driver: driver.find_element_by_xpath(xpath))

    def wait4xpath_s(self,time,xpath):
        self.logger.log("Waiting for element XPATH = " + xpath)
        return WebDriverWait(self.browser, time).until(lambda driver: driver.find_elements_by_xpath(xpath))

    def wait4id(self,time,id):
        self.logger.log("Waiting for element ID = " + id)
        return WebDriverWait(self.browser, time).until(lambda driver: driver.find_element_by_id(id))
