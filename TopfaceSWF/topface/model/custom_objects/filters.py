# coding=utf-8
from time import sleep
import traceback
from selenium.common.exceptions import NoSuchElementException
from engine.test_failed_exception import TestFailedException
from topface.model.custom_objects.profile import Profile
from topface.model.object_model import ObjectModel
import settings

__author__ = 'ngavrish'

class Filters(ObjectModel):

    _sex_filter_xpath = "//div[@id='ratingAllFilter']//a[contains(@class,'gender-filter')]"
    _online_filter_checkbox_id = "onlineFilter"
    _age_filter_link_xpath = "//a[contains(@class,'age-filter')]"
    _right_age_slider_xpath = ".//*[@id='slider']/a[2]"
    _select_goal_xpath = "//div[@id='widgetFilter']//span[contains(@class,'selectBox-label')]"
    _goal_status_xpath = "//div[@id='userPhotoLayout']//div[contains(@class,'"


    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def get_goal_status_xpath(self,goal):
        return self._goal_status_xpath + goal + "')]"

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

    def select_online(self):
        self.logger.log("Switch online filter")
        profile = Profile(self.browser,self.logger)
        self.click(
            self.get_element_by_id(self._online_filter_checkbox_id))
        self.wait4xpath(settings.wait_for_element_time,profile._online_indicator)

    def change_sex(self):
        self.logger.log("Change sex and return current filter value")
        sex_element = self.get_element_by_xpath(self._sex_filter_xpath)
        sex_before_change = sex_element.text
        self.hover(sex_element)
        self.click(sex_element)
        sex_after_change = sex_element.text
        sleep(2)
        self.logger.log("Comparing elements: " + sex_after_change + " vs " + sex_before_change)
        if sex_after_change == sex_before_change:
            raise TestFailedException("Failed to change sex")
        return sex_after_change

    def select_goal(self,goal):
        self.logger.log("Select goal")
        self.click(
            self.get_element_by_xpath(self._select_goal_xpath))
        goal_option = self.get_element_by_xpath("//a[@rel='" + goal + "']")
        self.hover(goal_option)
        self.click(goal_option)
        self.wait4xpath(settings.wait_for_element_time,
                        self.get_goal_status_xpath(goal))

    def validate(self,goal,online):
        profile = Profile(self.browser,self.logger)
        if online:
            self.wait4xpath(settings.wait_for_element_time,profile._online_indicator)
        try:
            self.logger.log("validating user goal status in search")
            self.wait4xpath(settings.wait_for_element_time,
                self.get_goal_status_xpath(goal))
        except Exception as e:
            raise TestFailedException("Failed to validate user from filter search with goal = " + str(goal) + "\n\r" +
                                      traceback.format_exc())