# coding=utf-8
import traceback
from engine.test_suite import TestSuite
from engine.test_case import TestCase
from topface import profiling_events
from topface.model.custom_objects.auth import AuthForm
from topface.model.custom_objects.browser_window import BrowserWindow
from topface.model.custom_objects.filters import Filters
from topface.model.custom_objects.js_popups.dreams_popup import DreamsPopup
from topface.model.custom_objects.marks import Marks
from topface.model.custom_objects.navigation import Navigation
from topface.model.custom_objects.profile import Profile
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.custom_objects.js_popups.leaders_baloon import LeadersBaloon
from topface.model.custom_objects.js_popups.none_found_in_search import NoneFoundInSearch
from topface.model.custom_objects.js_popups.vip_popups import VIPPopups

__author__ = 'ngavrish'


class MainFilterTestSuite(TestSuite):

    def __init__(self, name):
        TestSuite.__init__(self,name)
        self.browser_name = TestSuite.browser_name
        self.test_cases = []
        self.result = {}

    def run(self):
        self.test_cases = [
            self.MainAgeBar("Age_bar_depending_on_users_age"),
            self.MainNonVipGoalSexAndOnlineFilters("Validate_for_non_vip_goal_sex_online"),
            self.MainNonVipExtendedFilters("NonVipExtendedFilter")
        ]

        for test_case in self.test_cases:
            run_test_results = test_case.run_test(self.browser_name)
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        return {self.__class__.__name__: self.result}


    #noinspection PyMethodOverriding,PyMissingConstructor
    class MainAgeBar(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)
            self.ages_list = {17:4,18:4,20:4,21:5,24:5,25:5,26:6,29:6,30:6,31:8,99:8}

        def run(self, browser, logger):
            # Get local session of firefox
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
                navigation.goto_main()
                marks.star_box()
                filter.init_age_filter()
                print 100500
                filter.drag_right_age_search_slider_to_max()
                filter.drag_right_age_search_slider_to_min()
                if self.ages_list[age] != filter.get_age_search_interval_value():
                    raise TestFailedException("Wrong mininal age search interval")
            profile.set_age(auth.FilterUserNonVipVK.age)
            window.close()

    #noinspection PyMissingConstructor,PyMethodOverriding
    class MainNonVipGoalSexAndOnlineFilters(TestCase):
        def __init__(self,test_name):
            self.set_log_name(test_name)
            self.sexes_amount = 2
#            amount of users to check current filter settings
            self.validate_user_amount = 10

        def run(self,browser,logger):
            auth = AuthForm(browser,logger)
            filter = Filters(browser,logger)
            marks = Marks(browser,logger)
            dreams_popup = DreamsPopup(browser,logger)
            leaders_baloon = LeadersBaloon(browser,logger)
            window = BrowserWindow(browser, logger)

            window.open(settings.target_url)
            self.do_method(auth.login_with_vk_full_scale,profiling_events.login_event,auth.FilterUserNonVipVK)
            dreams_popup.close()
            leaders_baloon.close()
            leaders_baloon.close_want_fast_meet()
#            while True:
#                try:
#                    leaders_baloon.close()
#                except Exception:
#                    print "EXCEPTION"
#                    break
            filter.select_online()
            for sex in range(self.sexes_amount):
                filter.change_sex()
                for goal in filter.get_goals():
                    filter.select_goal(goal)
#                    checking for validate_user_amount filter is working
                    for i in range(self.validate_user_amount):
                        self.logger.log("Validating " + str(i) + "th user")
                        marks.like()
                        filter.validate_goal(goal=goal,online=True)
                        marks.mark()
            filter.change_sex()
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MainNonVipExtendedFilters(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)
            self.sexes_amount = 2
            #            amount of users to check current filter settings
            self.validate_user_amount = 10

        def run(self, browser, logger):
            auth = AuthForm(browser, logger)
            filter = Filters(browser, logger)
            marks = Marks(browser, logger)
            dreams_popup = DreamsPopup(browser, logger)
            leaders_baloon = LeadersBaloon(browser, logger)
            none_found_in_search = NoneFoundInSearch(browser,logger)
            navigation = Navigation(browser,logger)
            vip_popup = VIPPopups(browser,logger)
            window = BrowserWindow(browser, logger)

            self.do_method(auth.login_with_vk_full_scale, profiling_events.login_event, auth.FilterUserNonVipVK)
            dreams_popup.close()
            leaders_baloon.close()
            leaders_baloon.close_want_fast_meet()

            filter.expand_parameter_list()
            filter.collapse_parameter_list()
            filter.expand_parameter_list()
            filter.validate_default_extended_params()
            filter.expand_more_params_box()
            filter.collapse_more_params_box()

            extended_params = filter.get_extended_params()
            for param in extended_params:
                filter.add_param(param)
            self.logger.log("**********************************************")
            self.logger.log("One by one additional parameters were selected")
            self.logger.log("**********************************************")
            for param in extended_params:
                filter.remove_param(param)
            for param in extended_params:
                filter.add_param(param)
            self.logger.log("**********************************************")
            self.logger.log("One by one additional parameters were selected")
            self.logger.log("**********************************************")
            for param in filter.get_all_params():
#                default value = 1 is OK
                self.logger.log("Setting param with name = " + param)
                none_found_in_search.close()
                filter.set_filter_param_value(param)
# #9262 - popup when deleting filter
#            for param in extended_params:
#                filter.add_param(param)
            none_found_in_search.mark_everyone()
#9267 - second time getting none found popup
            none_found_in_search.mark_everyone()
            filter.expand_parameter_list()
            filter.expand_more_params_box()
            filter.set_filter_param_value(filter._default_visible_params[0])

            for i in range(10):
                marks.mark()
            marks.mark_and_validate_mark(
                marks.get_mark_by_value(9))
            marks.mark_and_validate_mark(
                marks.get_mark_by_value(10))

            navigation.goto_profile_from_search()
            vip_popup.close_premium()
            navigation.goto_profile_from_search(way="photo")
            vip_popup.close_premium()
            window.close()

    #noinspection PyMethodOverriding,PyMissingConstructor
    class MainVipExtendedFilters(TestCase):
        def __init__(self, test_name):
            self.set_log_name(test_name)
            self.sexes_amount = 2
            #            amount of users to check current filter settings
            self.validate_user_amount = 10

        def run(self, browser, logger):
            auth = AuthForm(browser, logger)
            filter = Filters(browser, logger)
            marks = Marks(browser, logger)
            dreams_popup = DreamsPopup(browser, logger)
            leaders_baloon = LeadersBaloon(browser, logger)
            none_found_in_search = NoneFoundInSearch(browser,logger)
            navigation = Navigation(browser,logger)
            vip_popup = VIPPopups(browser,logger)
            window = BrowserWindow(browser, logger)

            self.do_method(auth.login_with_vk_full_scale, profiling_events.login_event, auth.FilterUserNonVipVK)
            dreams_popup.close()
            leaders_baloon.close()
            leaders_baloon.close_want_fast_meet()
