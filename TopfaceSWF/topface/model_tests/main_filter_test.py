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

__author__ = 'ngavrish'


class MainFilterTestSuite(TestSuite):

    def __init__(self, name):
        TestSuite.__init__(self,name)
        self.browser_name = TestSuite.browser_name
        self.test_cases = []
        self.result = {}

    def run(self):
        self.test_cases = [
            self.AgeBar("Age_bar_depending_on_users_age"),
            self.NonVipGoalSexAndOnlineFilters("Validate_for_non_vip_goal_sex_online")
        ]

        for test_case in self.test_cases:
            run_test_results = test_case.run_test(self.browser_name)
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        return {self.__class__.__name__: self.result}


    #noinspection PyMethodOverriding,PyMissingConstructor
    class AgeBar(TestCase):
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
    class NonVipGoalSexAndOnlineFilters(TestCase):
        def __init__(self,test_name):
            self.set_log_name(test_name)
            self.goals=["love",
                        "sex",
                        "friend",
                        "estimates",
                        "talk"]
            self.sexes_amount = 2
#            amount of users to check current filter settings
            self.validate_user_amount = 10

        def run(self,browser,logger):
            auth = AuthForm(browser,logger)
            filter = Filters(browser,logger)
            marks = Marks(browser,logger)
            dreams_popup = DreamsPopup(browser,logger)
            leaders_baloon = LeadersBaloon(browser,logger)

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
                sex = filter.change_sex()
                for goal in self.goals:
                    filter.select_goal(goal)
#                    checking for validate_user_amount filter is working
                    for i in range(self.validate_user_amount):
                        self.logger.log("Validating " + str(i) + "th user")
                        marks.like()
                        filter.validate(goal=goal,online=True)
                        marks.mark()


