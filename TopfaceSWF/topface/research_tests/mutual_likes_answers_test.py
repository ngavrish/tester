# coding=utf-8
from engine.test_case import TestCase
from engine.test_suite import TestSuite
from engine.test_failed_exception import TestFailedException
from topface.model.browser_window import BrowserWindow
import settings
from topface.model.auth import AuthForm
from topface.model.filters import Filters
from topface.model.marks import Marks
from topface.model.messanger import Messenger
from topface.model.navigation import Navigation
from topface import profiling_events

__author__ = 'ngavrish'

class MutualLikeAnswersTestSuite(TestSuite):

    def run(self):
        """
        TestCases = names of VK users
        This allows us to create perconal research for every type of user
        Now it would be just written in stone.
        Brought to some dynamic datastorage like MySQL later
        """
        test_cases = [
            self.Male_24_Moskow("Male_24_Moskow_MutualLike_Answers")
        ]

        for test_case in test_cases:
            test_case.run_test()


    #noinspection PyMethodOverriding,PyMissingConstructor,PyArgumentList
    class Male_24_Moskow(TestCase):
        """

        """
        _root_window = None

        def __init__(self, test_name):
            self.set_log_name(test_name)

        def run(self, browser, logger):
            # Get local session of firefox
            window = BrowserWindow(browser, logger)
            auth = AuthForm(self.browser,self.logger)
            filters = Filters(self.browser,self.logger)
            marks = Marks(self.browser,self.logger)
            navigation = Navigation(self.browser,self.logger)
            messenger = Messenger(self.browser,self.logger)

            self.do_method(auth.login_with_vk_full_scale,profiling_events.events[profiling_events.login_event],auth.MSK_24_Male)
            filters.change_online_filter_value()
#            User's profiles, that i've liked. Amount of that users is now stored in settings.like_amount
            users_liked = marks.like_users_from_main(settings.like_amount)
#            Users that liked me back. no matter, did I liked them during this test, or another
            mutual_users = marks.get_mutual_profiles()
            self.logger.log("Users I liked = " + str(users_liked))
            self.logger.log("Mutual users = " + str(mutual_users))
            liked_who_i_liked = []
#            Getting users who gave me mutual like after I liked them during this particular test
            for user in users_liked:
                if user in mutual_users:
                    liked_who_i_liked.append(user)
            self.logger.log("MALE USER 24 YEARS OLD, MOSKOW. Mutual likes for N minutes = " + str(len(liked_who_i_liked)))
            print "MALE USER 24 YEARS OLD, MOSKOW. Mutual likes for N minutes = " + str(liked_who_i_liked)

            for user in liked_who_i_liked:
                navigation.goto_messenger_from_mutual_likes(user)
                self._root_window = self.browser.current_window_handle
                messenger.send_and_validate_message(u"Привет! :) Давай знакомиться ;)")
                window.switch_to_popup()
            self.logger.log("Amount of final answered messages = " + str(len(marks.get_answered_messages(liked_who_i_liked))))
            window.close()

