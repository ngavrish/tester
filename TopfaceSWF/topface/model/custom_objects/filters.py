# coding=utf-8
from time import sleep
import traceback
from selenium.common.exceptions import NoSuchElementException
from engine.test_failed_exception import TestFailedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from topface.model.custom_objects.marks import Marks
from topface.model.custom_objects.profile import Profile
from topface.model.object_model import ObjectModel
import settings

__author__ = 'ngavrish'

class Filters(ObjectModel):

    _sex_filter_xpath = "//div[@id='ratingAllFilter']//a[contains(@class,'gender-filter')]"
    _online_filter_checkbox_id = "onlineFilter"
    _age_filter_link_xpath = "//a[contains(@class,'age-filter')]"
    _right_age_slider_xpath = ".//*[@id='slider']/a[2]"
    _left_age_slider_xpath = ".//*[@id='slider']/a[1]"
    _select_goal_xpath = "//div[@id='widgetFilter']//span[contains(@class,'selectBox-label')]"
    _goal_status_xpath = "//div[@id='userPhotoLayout']//div[contains(@class,'"
    _expand_params_id = "extendedFilterMore"
    _collapse_params_id = "extendedFilterLess"
    _extended_param_div_id = "WidgetExtendedFilter"
    _extended_expanded_param_div_xpath = "//div[@id='WidgetExtendedFilter' and @style='display: block;']"
    _extended_collapsed_param_div_xpath = "//div[@id='WidgetExtendedFilter' and @style='display: none;']"
    _visible_default_params_xpath = "//div[(contains(@class,'param-even') or (contains(@style,'block') and contains(@class,'extended-filter-param'))) and not(contains(@style,'display: none;')) and not(contains(@class,'hidden'))]"
    _visible_params_xpath = "//div[(contains(@class,'param-even') or (contains(@style,'block') and contains(@class,'extended-filter-param')))]"
    _additional_xpath_for_delete_button = "//div[@class='delete-param-button']"
    _add_more_params_link_id = "filterAddMoreParams"
    _more_params_box_id = "addMoreSearchParams"
    _expanded_addmoreparams_box_xpath = "//div[@id='addMoreSearchParams' and contains(@style,'display: block')]"
    _collapsed_addmoreparams_box_xpath = "//div[@id='addMoreSearchParams' and contains(@style,'display: none')]"
    _close_more_params_box_xpath = "//div[@id='addMoreSearchParams']/div[contains(@class,'close')]"
    _more_params_div_by_param_xpath = "//div[@id='addMoreSearchParams']//div[@name='"#']"
    _add_more_params_button_xpath = ".//*[@id='addMoreSearchParams']/div[@class='ok']"
    _addmore_params_item_xpath = "//div[@id='addMoreSearchParams']//div[@class='extended-param-list-item' and @name='"
    _additional_xpath_for_currently_selected_value = "//span[contains(@class,'selectBox-label')  and not(contains(@class,'zero-option'))]"

    _goals =    ["love",
                "sex",
                "friend",
                "estimates",
                "talk"]
    _default_visible_params = ["marriage",
                               "character",
                               "breast",
                               "alcohol"]
    _extended_params = ["job",
                        "status",
                        "education",
                        "finances",
                        "smoking",
                        "communication",
                        "hairColor",
                        "eyeColor",
                        "children",
                        "residence",
                        "hasCar"]
    _param_order_map = {
        "marriage": 4,
        "character": 6,
        "alcohol": 8,
        "breast": 16,
        "job": 1,
        "status": 2,
        "education": 3,
        "finances": 5,
        "smoking": 7,
        "communication": 10,
        "hairColor": 11,
        "eyeColor": 12,
        "children": 13,
        "residence": 14,
        "hasCar": 15,
    }

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def get_addmoreelement_by_param_name(self,param):
        return self.get_element_by_xpath(
            self._addmore_params_item_xpath + param + "']")

    def get_extended_param_ul_xpath_by_praram_name(self,param):
        self.logger.log("For " + param + " div order number = " + str(self._param_order_map[param]))
        try:
            ul_order_number = self._param_order_map[param]
            return "//ul[contains(@class,'extended-filter-answers-selectBox-dropdown-menu answers-0-selectBox-')][" +\
                   str(ul_order_number) + "]"
        except Exception as e:
            raise TestFailedException("Failed to get_extended_param_ul_xpath_by_praram_name \n\r" + traceback.format_exc())

    def get_visible_param_xpath_by_param_name(self,param):
        return "//div[(contains(@class,'param-even') and contains(@class,'extended-filter-param-" + \
               param + \
               "')) or (contains(@style,'block') and contains(@class,'extended-filter-param-" +\
               param + \
               "'))]"

    def get_extended_params_list_item_xpath_by_param_name(self,param,value):
        xpath = self.get_extended_param_ul_xpath_by_praram_name(param) +\
                "//li[contains(@class,'extended-filter-option')]/a[@rel=" + str(value) + "]"
        self.logger.log("Extended param item list = " + xpath)
        return xpath

    def get_extended_params(self):
        return self._extended_params

    def get_goals(self):
        return self._goals

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
        try:
            self.drag_and_drop(
                self.get_element_by_xpath(self._right_age_slider_xpath),
                400,0)
        except Exception:
            TestFailedException("Failed to drage age slider to the right maximum")

    def drag_right_age_search_slider_forward(self,years):
        try:
            self.drag_and_drop(
                self.get_element_by_xpath(self._right_age_slider_xpath),
                years*5,0)
        except Exception:
            TestFailedException("Failed to drage age slider to the right minimum")

    def drag_right_age_search_slider_backward(self,years):
        try:
            self.drag_and_drop(
                self.get_element_by_xpath(self._right_age_slider_xpath),
                years*(-5),0)
        except Exception:
            TestFailedException("Failed to drage age slider to the right minimum")

    def drag_right_age_search_slider_to_min(self):
        try:
            self.drag_and_drop(
                self.get_element_by_xpath(self._right_age_slider_xpath),
                -400,0)
        except Exception:
            TestFailedException("Failed to drage age slider to the right minimum")

    def drag_left_age_search_slider_forward(self,years=1):
        try:
            self.drag_and_drop(
                self.get_element_by_xpath(self._left_age_slider_xpath),
                years*5,0)
        except Exception:
            TestFailedException("Failed to drage age slider to the right maximum")

    def drag_left_age_search_slider_backward(self,years):
        try:
            self.drag_and_drop(
                self.get_element_by_xpath(self._left_age_slider_xpath),
                years*(-5),0)
        except Exception:
            TestFailedException("Failed to drage age slider to the right maximum")

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

    def get_age_search_interval_list(self):
        try:
            age_margin_value = self.get_element_by_xpath(self._age_filter_link_xpath).text
            self.logger.log(age_margin_value.encode('utf8'))
            start_age = int(age_margin_value[0:2])
            self.logger.log("Age start = " + str(start_age))
            end_age = int(age_margin_value[3:5])
            self.logger.log("Age end = " + str(end_age))
            return [end_age,end_age - start_age]
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

    def validate_goal(self,goal,online):
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

    def expand_parameter_list(self):
        self.logger.log("Expanding params list")
        self.hover(
            self.get_element_by_id(self._expand_params_id))
        self.click(
            self.get_element_by_id(self._expand_params_id))
        self.wait4xpath(settings.wait_for_element_time,self._extended_expanded_param_div_xpath)

    def collapse_parameter_list(self):
        self.logger.log("Collapsing params list")
        self.hover(
            self.get_element_by_id(self._collapse_params_id))
        self.click(
            self.get_element_by_id(self._collapse_params_id))
        self.wait4xpath(settings.wait_for_element_time,self._extended_collapsed_param_div_xpath)

    def validate_default_extended_params(self):
        self.logger.log("Validating default extended params")
        default_visible_elements = self.get_elements_by_xpath(self._visible_default_params_xpath)
        if len(default_visible_elements) != len(self._default_visible_params):
            self.logger.log("Found default visible elements amount = " + str(len(default_visible_elements)))
            self.logger.log("Expected = " + str(len(self._default_visible_params)))
            raise TestFailedException("Failed to validate amount of params that are visible by default")
        for param in self._default_visible_params:
            self.wait4xpath(settings.wait_for_element_time,self.get_visible_param_xpath_by_param_name(param))

    def expand_more_params_box(self):
        self.hover(
            self.get_element_by_id(self._add_more_params_link_id))
        self.click(
            self.get_element_by_id(self._add_more_params_link_id))
        try:
            self.get_element_by_id(self._more_params_box_id).get_attribute("style")
            self.wait4xpath(settings.wait_for_element_time,self._expanded_addmoreparams_box_xpath)
        except Exception as e:
            raise TestFailedException("Failed to validate add more params box")

    def collapse_more_params_box(self):
        self.logger.log("Collapsing more params box")
        self.hover(
            self.get_element_by_xpath(self._close_more_params_box_xpath))
        self.click(
            self.get_element_by_xpath(self._close_more_params_box_xpath))
        try:
            self.get_element_by_id(self._more_params_box_id).get_attribute("style")
            self.wait4xpath(settings.wait_for_element_time,self._collapsed_addmoreparams_box_xpath)
        except Exception as e:
            raise TestFailedException("Failed to validate add more params box")

    def add_param(self,param):
        self.expand_more_params_box()
        param2add = self.get_element_by_xpath(self._more_params_div_by_param_xpath + param + "']")
        self.hover(param2add)
        self.click(param2add)
        self.click(
            self.get_element_by_xpath(self._add_more_params_button_xpath))
        self.wait4xpath(settings.wait_for_element_time,self.get_visible_param_xpath_by_param_name(param))
        self.expand_more_params_box()
        try:
            self.wait4xpath(settings.wait_for_element_time,self._more_params_div_by_param_xpath + param + "']")
            raise TestFailedException("Element that've been added to filter list still exists in add more params = " + param)
        except Exception:
#            element shouldn't be found
            self.collapse_more_params_box()

    def remove_param(self,param):
        self.logger.log("Removing element with param = " + param)
        try:
            close_xpath = self.get_visible_param_xpath_by_param_name(param) + self._additional_xpath_for_delete_button
            self.logger.log("Element xpath = " + close_xpath)
            close_element = self.get_element_by_xpath(close_xpath)
            self.hover(
                self.get_element_by_xpath(
                    self.get_visible_param_xpath_by_param_name(param)))
            self.click(close_element)
            self.expand_more_params_box()
            self.wait4xpath(settings.wait_for_element_time,self._more_params_div_by_param_xpath + param + "']")
            self.collapse_more_params_box()
        except Exception as e:
            raise TestFailedException("Failed to remove params \n\r" + traceback.format_exc())

#    NOT WORKING
#    def add_all_params(self):
#        self.logger.log("Using CONTROL button selecint all elements")
#        try:
#            self.expand_more_params_box()
#            ActionChains(self.browser).key_down(Keys.CONTROL)\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[0]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[1]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[2]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[3]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[4]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[5]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[6]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[7]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[8]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[9]))\
#                        .click(self.get_addmoreelement_by_param_name(self._extended_params[10]))\
#                        .key_up(Keys.CONTROL).perform()
#            self.key_up(Keys.CONTROL)
#            self.click(
#                self.get_element_by_xpath(self._add_more_params_button_xpath))
#        except Exception as e:
#            raise TestFailedException("Failed to add all params with controrl button \n\r" + traceback.format_exc())

    def get_all_params(self):
        self.logger.log("Getting all parameters")
        return self._default_visible_params + self._extended_params

    def set_filter_param_value(self,param,value=1):
        self.logger.log("Set filter param = " + str(param) + " value = " + str(value))
        self.click(
            self.get_element_by_xpath(
                self.get_visible_param_xpath_by_param_name(param)))
        self.hover(
            self.get_element_by_xpath(
                self.get_extended_params_list_item_xpath_by_param_name(param,value)))
        self.click(
            self.get_element_by_xpath(
                self.get_extended_params_list_item_xpath_by_param_name(param,value)))

    def unset_filter_param_value(self,param):
        self.logger.log("Set filter param = " + str(param) + " value = 0")
        self.click(
            self.get_element_by_xpath(
                self.get_visible_param_xpath_by_param_name(param)))
        self.hover(
            self.get_element_by_xpath(
                self.get_extended_params_list_item_xpath_by_param_name(param,0)))
        self.click(
            self.get_element_by_xpath(
                self.get_extended_params_list_item_xpath_by_param_name(param,0)))

    def get_param_description(self,param):
        self.logger.log("Getting 0 value param = " + str(param) + " description ")
        try:
            self.click(
                self.get_element_by_xpath(
                    self.get_visible_param_xpath_by_param_name(param)))
            descriptor_element = self.get_element_by_xpath(
                self.get_extended_params_list_item_xpath_by_param_name(param,0))
            self.logger.log("Descriptor text = " + descriptor_element.text)
            return descriptor_element.text
        except Exception:
            raise TestFailedException("Failed to get param " + param + " description " + traceback.format_exc())

    def get_selected_param(self,param):
        self.logger.log("Selecting selected param value")
        try:
            return self.get_element_by_xpath(
                self.get_visible_param_xpath_by_param_name(param) +
                    self._additional_xpath_for_currently_selected_value)
        except Exception:
            raise TestFailedException("Failed to get currently selected value for param = " + param)


    def validate_user_in_search_age(self,age_interval):
        marks = Marks(self.browser,self.logger)
        age = int(marks.get_user_age())
        if age < age_interval[1] or age > age_interval[0] + age_interval[1]:
            raise TestFailedException("Failed to validate user age \r\n Found age = " + str(age) +
                                      "\r\n Expected interval: " + str(age_interval))

