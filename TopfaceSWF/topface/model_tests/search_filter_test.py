# coding=utf-8
from engine.test_failed_exception import TestFailedException
from engine.test_suite import TestSuite
from topface import profiling_events
from engine.test_case import TestCase
from topface.model.custom_objects.auth import AuthForm
import settings
from topface.model.custom_objects.marks import Marks
from topface.model.custom_objects.filters import Filters
from topface.model.custom_objects.profile import Profile
from topface.model.custom_objects.navigation import Navigation
from topface.model.custom_objects.browser_window import BrowserWindow

__author__ = 'ngavrish'

class SearchFilterTestSuite(TestSuite):

    def __init__(self, name):
        TestSuite.__init__(self,name)
        self.browser_name = TestSuite.browser_name
        self.test_cases = []
        self.result = {}

    def run(self):
        self.test_cases = [
           # self.AgeBar("DatingAgeBar"),
            self.AgeBarValidateSearch("AgeBarValidateSearch")
            #            self.MainVipExtendedFilters("VipExtendedFilters")
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
                filter.validate_search_users_in_search_age([age,age+self.ages_list[age]])
                if self.ages_list[age] != filter.get_age_search_interval_value():
                    raise TestFailedException("Wrong mininal age search interval")
            profile.set_age(auth.FilterUserNonVipVK.age)
            window.close()
