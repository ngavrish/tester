# coding=utf-8
from time import sleep
from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite
from topface import profiling_events
from engine.test_case import TestCase
from topface.model.custom_objects.auth import AuthForm
from topface.model.custom_objects.js_popups.dreams_popup import DreamsPopup
from topface.model.custom_objects.search_box import SearchBox
import settings
from topface.model.custom_objects.marks import Marks
from topface.model.custom_objects.filters import Filters
from topface.model.custom_objects.profile import Profile
from topface.model.custom_objects.navigation import Navigation
from topface.model.custom_objects.browser_window import BrowserWindow
from topface.model.custom_objects.js_popups.leaders_baloon import LeadersBaloon

__author__ = 'ngavrish'

class SearchFilterTestSuite(TestSuite):

    def __init__(self, name):
        TestSuite.__init__(self,name)
        self.browser_name = TestSuite.browser_name
        self.test_cases = []
        self.result = {}

    def run(self):
        self.test_cases = [
#           self.AgeBar("DatingAgeBar"),
#           self.AgeBarValidateSearch("AgeBarValidateSearch"),
#           self.AgeBarYearByYearMinimumInterval2LeftValidateSearch("Search_Age_Bar_Year_By_Year_Minimum_Interval_"+
#                                                                   "to_Left_Validate_Search"),
#           self.AgeBarYearByYearMinimumInterval2RightValidateSearch("Search_Age_Bar_Year_By_Year_Minimum_Interval_"+
#                                                                    "to_Right_Validate_Search"),
           self.NonVipGoalSexAndOnlineFilters("Non_Vip_Goal_Sex_And_Online_Filters")
#                        self.MainVipExtendedFilters("VipExtendedFilters")
        ]
        for test_case in self.test_cases:
            run_test_results = test_case.run_test(self.browser_name)
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        return {self.__class__.__name__: self.result}


    #noinspection PyMethodOverriding,PyMissingConstructor
    class AgeBar(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)
            self.search_url = "/search/"
            self.ages_list = {17:4,18:4,20:4,21:5,24:5,25:5,26:6,29:6,30:6,31:8,99:8}

        def run(self, browser, logger):
            # Get local session of firefox
            window = BrowserWindow(browser, logger)
            auth = AuthForm(browser,logger)
            navigation = Navigation(browser,logger)
            profile = Profile(browser,logger)
            filter = Filters(browser,logger)

            window.open(settings.target_url)
            #            implement URL check
            self.do_method(auth.login_with_vk_full_scale,profiling_events.login_event,auth.FilterUserNonVipVK)
            for age in self.ages_list:
                self.logger.log("For age = " + str(age) + " search age interval = " + str(self.ages_list[age]))
                profile.set_age(age)
                navigation.goto_main_top_menu_item(u"Знакомства")
                navigation.validate_in_search()
                filter.init_age_filter()
                filter.drag_right_age_search_slider_to_max()
                filter.drag_right_age_search_slider_to_min()
                if self.ages_list[age] != filter.get_age_search_interval_value():
                    raise TestFailedException("Wrong mininal age search interval")
            profile.set_age(auth.FilterUserNonVipVK.age)
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class AgeBarValidateSearch(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)
            self.ages_list = {17:4,18:4,20:4,21:5,24:5,25:5,26:6,29:6,30:6,31:8,99:8}

        def run(self,browser,logger):
            self.browser = browser
            self.logger = logger
            window = BrowserWindow(browser, logger)
            auth = AuthForm(browser,logger)
            navigation = Navigation(browser,logger)
            profile = Profile(browser,logger)
            filter = Filters(browser,logger)
            marks = Marks(browser,logger)

            window.open(settings.target_url)
            #            implement URL check
            self.do_method(auth.login_with_vk_full_scale,profiling_events.login_event,auth.FilterUserNonVipVK)
            for age in self.ages_list:
                self.logger.log("For age = " + str(age) + " search age interval = " + str(self.ages_list[age]))
                profile.set_age(age)
                navigation.goto_main_top_menu_item(u"Знакомства")
                navigation.validate_in_search()
                filter.init_age_filter()
                filter.drag_right_age_search_slider_to_max()
                filter.drag_right_age_search_slider_to_min()
                filter.validate_search_users_in_search_age(filter.get_age_search_interval_list())
                if self.ages_list[age] != filter.get_age_search_interval_value():
                    raise TestFailedException("Wrong mininal age search interval")
            profile.set_age(auth.FilterUserNonVipVK.age)
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class AgeBarYearByYearMinimumInterval2LeftValidateSearch(TestCase):
    #    year by year using minimal interval from left to maximum
        def __init__(self, test_name):
            self.set_log_name(test_name)
            self.age_min_min = 16
            self.age_min_max = 72

        def run(self, browser, logger):
            self.browser = browser
            self.logger = logger
            window = BrowserWindow(browser, logger)
            auth = AuthForm(browser,logger)
            navigation = Navigation(browser,logger)
            profile = Profile(browser,logger)
            filter = Filters(browser,logger)
            marks = Marks(browser,logger)

            window.open(settings.target_url)
            #            implement URL check
            self.do_method(auth.login_with_vk_full_scale,profiling_events.login_event,auth.FilterUserNonVipVK)
            profile.set_age(self.age_min_min)
            navigation.goto_main_top_menu_item(u"Знакомства")
            filter.init_age_filter()
            filter.drag_right_age_search_slider_to_max()
            filter.drag_right_age_search_slider_to_min()
            for age in range(self.age_min_max-self.age_min_min):
                filter.init_age_filter()
                filter.drag_left_age_search_slider_forward()
                filter.validate_search_users_in_search_age(filter.get_age_search_interval_list())
            profile.set_age(auth.FilterUserNonVipVK.age)
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class AgeBarYearByYearMinimumInterval2RightValidateSearch(TestCase):
    #    year by year using minimal interval from
        def __init__(self, test_name):
            self.set_log_name(test_name)
            self.age_min = 16
            self.age_max_min = 20
            self.age_max_max = 80

        def run(self, browser, logger):
            self.browser = browser
            self.logger = logger
            window = BrowserWindow(browser, logger)
            auth = AuthForm(browser,logger)
            navigation = Navigation(browser,logger)
            profile = Profile(browser,logger)
            filter = Filters(browser,logger)
            marks = Marks(browser,logger)

            window.open(settings.target_url)
            #            implement URL check
            self.do_method(auth.login_with_vk_full_scale,profiling_events.login_event,auth.FilterUserNonVipVK)
            profile.set_age(self.age_min)
            navigation.goto_main_top_menu_item(u"Знакомства")
            filter.init_age_filter()
            filter.drag_left_age_search_slider_to_max()
            sleep(5)
            for age in reversed(range(self.age_max_max-self.age_max_min)):
                filter.init_age_filter()
                filter.drag_right_age_search_slider_backward()
                sleep(5)
                filter.validate_search_users_in_search_age(filter.get_age_search_interval_list())
            profile.set_age(auth.FilterUserNonVipVK.age)
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class NonVipGoalSexAndOnlineFilters(TestCase):
        def __init__(self,test_name):
            self.set_log_name(test_name)
            self.sexes_amount = 2
            self.minimal_age_interval = 50
            #            amount of users to check current filter settings

        def run(self,browser,logger):
            auth = AuthForm(browser,logger)
            filter = Filters(browser,logger)
            navigation = Navigation(browser,logger)
            window = BrowserWindow(browser, logger)

            window.open(settings.target_url)
            self.do_method(auth.login_with_vk_full_scale,profiling_events.login_event,auth.FilterUserNonVipVK)
            navigation.goto_main_top_menu_item(u"Знакомства")
            filter.init_age_filter()
            if filter.get_age_search_interval_value() < self.minimal_age_interval:
                filter.drag_left_age_search_slider_to_min()
                sleep(5)
                filter.drag_right_age_search_slider_to_max()
            filter.close_age()
            filter.select_online()
            for sex in range(self.sexes_amount):
                filter.change_sex()
                for goal in filter.get_goals():
                    filter.select_goal(goal)
                    #                    checking for validate_user_amount filter is working
                    self.logger.log("Validating users in search box")
                    filter.validate_in_search_goal(goal=goal,online=True)
            filter.change_sex()
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class NonVipExtendedFilters(TestCase):
        def __init__(self,test_name):
            self.set_log_name(test_name)
            self.sexes_amount = 2
            self.minimal_age_interval = 50
            #            amount of users to check current filter settings

        def run(self,browser,logger):
            auth = AuthForm(browser,logger)
            filter = Filters(browser,logger)
            navigation = Navigation(browser,logger)
            window = BrowserWindow(browser, logger)

            window.open(settings.target_url)
            self.do_method(auth.login_with_vk_full_scale,profiling_events.login_event,auth.FilterUserNonVipVK)
            navigation.goto_main_top_menu_item(u"Знакомства")
            filter.init_age_filter()
            if filter.get_age_search_interval_value() < self.minimal_age_interval:
                filter.drag_left_age_search_slider_to_min()
                sleep(5)
                filter.drag_right_age_search_slider_to_max()
            filter.close_age()

