# coding=utf-8
from engine.test_case import TestCase
from engine.test_suite import TestSuite
from topface.model.auth import AuthForm
from topface.model.browser_window import BrowserWindow
from topface.model.navigation import Navigation
from topface.model.js_popups.fans_popups import FansPopups
from topface.model.js_popups.guests_popups import GuestsPopups
from topface.model.profile import Profile

__author__ = 'ngavrish'

class ProfileTestSuite(TestSuite):

    def run(self):
        test_cases = [
            self.ProfileNavigationTest("Profile_Navigation_Test")
        ]
        for test_case in test_cases:
            test_case.run_test()

    class ProfileNavigationTest(TestCase):

        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            """

            """
            auth = AuthForm(self.browser, self.logger)
            window = BrowserWindow(self.browser,self.logger)
            navigation = Navigation(self.browser,self.logger)
            profile = Profile(self.browser,self.logger)
            fans_popup = FansPopups(self.browser,self.logger)
            guests_popup = GuestsPopups(self.browser,self.logger)

            auth.login_with_fb_full_scale(auth.User1)
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
            fans_popup.validate_fans_forbidden_nonvip()
            self.browser.back()
            navigation.goto_tab_menu_item(u"Гости")
            guests_popup.validate_guests_forbidden_nonvip()
            self.browser.back()
            navigation.goto_tab_menu_item(u"Гороскоп")
            profile.validate_horo_view()





    class ProfileAnketEditingTest(TestCase):

        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):
            pass

    class ProfileSettingsEditingTest(TestCase):

        def __init__(self,test_name):
            self.set_log_name(test_name)

        def run(self,browser,logger):
            pass
