# coding=utf-8
from engine.test_case import TestCase
from engine.test_suite import TestSuite
from topface import profiling_events
from topface.model.custom_objects.auth import AuthForm
from topface.model.custom_objects.browser_window import BrowserWindow
from topface.model.custom_objects.marks import Marks
from topface.model.custom_objects.navigation import Navigation
from topface.model.custom_objects.profile import Profile
from topface.model.custom_objects.questionary import Questionary
from topface.model.custom_objects.js_popups.vip_popups import VIPPopups

__author__ = 'ngavrish'

class ProfileTestSuite(TestSuite):

    def __init__(self,name):
        TestSuite.__init__(self,name)
        self.browser_name = TestSuite.browser_name
        self.test_cases = []
        self.result = {}

    def run(self):
        self.test_cases = [
            self.ProfileNavigationTest("Profile_Navigation_Test"),
            self.QuestionaryEditingTest("Profile Anket Editing Test")
        ]
        for test_case in self.test_cases:
            run_test_results = test_case.run_test(self.browser_name)
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        return {self.__class__.__name__: self.result}

    class ProfileNavigationTest(TestCase):

        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            auth = AuthForm(self.browser, self.logger)
            window = BrowserWindow(self.browser,self.logger)
            navigation = Navigation(self.browser,self.logger)
            profile = Profile(self.browser,self.logger)
            vip_popup = VIPPopups(self.browser,self.logger)
            marks = Marks(self.browser, self.logger)

            self.do_method(auth.login_with_fb_full_scale,profiling_events.login_event,auth.User1)
            navigation.goto_top_menu_item(u"Профиль")
            profile.validate_profile_view()
            print "Profile view is validated"
            navigation.goto_tab_menu_item(u"Настройки")
            profile.validate_settings_view()
            print "Settings view is validated"
            navigation.goto_tab_menu_item(u"Уведомления")
            profile.validate_notifications_view()
            print "Notifications view is validated"
            navigation.goto_tab_menu_item(u"Контакты")
            profile.validate_contacts_view()
            navigation.goto_tab_menu_item(u"Фото")
            profile.validate_photo_view()
            navigation.goto_tab_menu_item(u"Поклонники")
            vip_popup.validate_forbidden_nonvip()
            self.browser.back()
            navigation.goto_tab_menu_item(u"Гости")
            vip_popup.validate_forbidden_nonvip()
            self.browser.back()
            navigation.goto_tab_menu_item(u"Гороскоп")
            profile.validate_horo_view()
#            logout and login with another user to mark that user again to fix the profile marks reset
            window.logout()
            self.do_method(auth.login_with_vk_full_scale,profiling_events.events[profiling_events.login_event],auth.User1)
#            navigate to resetted user profile
            window.open(auth.User1.profile_url_fb)

            for i in range(profile.marks_after_reset_amount):
                marks.click(
                    marks.get_mark_by_value(i+1)
                )
                marks.validate_profile_mark_sent()
                window.open(auth.User1.profile_url_fb)

            window.close()


    class QuestionaryEditingTest(TestCase):

        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):
            auth = AuthForm(self.browser, self.logger)
            window = BrowserWindow(self.browser,self.logger)
            navigation = Navigation(self.browser,self.logger)
            questionary = Questionary(self.browser,self.logger)

            self.do_method(auth.login_with_fb_full_scale,profiling_events.login_event,auth.User1)
            navigation.goto_top_menu_item(u"Профиль")
            questionary.expand()
            questionary.hide()
            questionary.expand()
            questionary.cancel()
            questionary.expand()
            questionary.uncheck_all_countries()
            questionary.save()
            questionary.validate_error_msg_wrong_data()
            questionary.fill_first_14_elements()
            questionary.save()
            questionary.validate_error_msg_answers_not_enough()
            questionary.check_dropdowns_to_input_transformation()
            questionary.fill_all()
            questionary.save()
            questionary.validate_saved_correctly()
            navigation.goto_top_menu_item(u"Профиль")
            questionary.expand()
            questionary.validate_filled_all()
            questionary.unfill_all()
            questionary.save()

            window.close()


    class ProfileSettingsEditingTest(TestCase):

        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):
            pass
