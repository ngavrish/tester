# coding=utf-8
import traceback
from selenium.common.exceptions import NoSuchElementException
from engine.test_failed_exception import TestFailedException
from topface.model.object_model import ObjectModel
import settings

__author__ = 'ngavrish'

class Filters(ObjectModel):

    _online_filter_checkbox_id = "onlineFilter"
    _age_filter_link_xpath = "//a[contains(@class,'age-filter')]"
    _right_age_slider_xpath = ".//*[@id='slider']/a[2]"


    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def change_online_filter_value(self):
        self.logger.log("Changing online-filter status")
        try:
            self.click(
                self.get_element_by_id(
                    self._online_filter_checkbox_id))
        except NoSuchElementException as e:
            raise TestFailedException("Failed to change online/offline filter status " + e.message)

    def init_age_filter(self):
        self.logger.log("Initialize age filter")
        self.hover(
            self.get_element_by_xpath(self._age_filter_link_xpath))
        self.click(
            self.get_element_by_xpath(self._age_filter_link_xpath))

    def drag_right_age_search_slider_to_max(self):
        self.logger.log("100500")
        self.drag_and_drop(
            self.get_element_by_xpath(self._right_age_slider_xpath),
            400,0)

    def drag_right_age_search_slider_to_min(self):
        self.drag_and_drop(
            self.get_element_by_xpath(self._right_age_slider_xpath),
            -400,0)

    def get_age_search_interval_value(self):
        try:
            age_margin_value = self.get_element_by_xpath(self._age_filter_link_xpath).text
            self.logger.log(age_margin_value.encode('utf8'))
            start_age = int(age_margin_value[0:2])
            self.logger.log("Age start = " + str(start_age))
            end_age = int(age_margin_value[3:5])
            self.logger.log("Age end = " + str(end_age))
            return end_age - start_age
        except Exception as e:
            raise TestFailedException(traceback.format_exc())