from topface.model.object_model import ObjectModel
from engine.test_failed_exception import TestFailedException

__author__ = 'ngavrish'

class SearchBox(ObjectModel):

    _user_items_xpath = "//div[@id='searchList']//div[@class='user-item']"
    _user_items_name_xpath = "//div[@class='userItemName']"
    _user_profile_link_xpath = "//a[@class='profileButton']"
    _user_online_icon_xpath = "//div[contains(@class,'onlineOnPhoto') or contains(@class,'onlineTrayOnPhoto') or contains(@class,'onlineMobileOnPhoto')]"
    _user_goal_beginning_xpath = "//div[contains(@class,'"

    def __init__(self, browser, logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def get_users_profile_age_dict(self):
        self.logger.log("Gettings users age list")
        users_count = len(self.get_elements_by_xpath(self._user_items_xpath))
        age_profile_dict = {}
        try:
            for i in range(users_count):
                buf_xpath = self._user_items_xpath + "[" + str(i+1) + "]"
                user = self.get_element_by_xpath(buf_xpath)
                self.hover(user)
                try:
                    name = self.get_element_by_xpath(buf_xpath + self._user_items_name_xpath)
                    profile = self.get_element_by_xpath(buf_xpath + self._user_profile_link_xpath)
                    age = int(name.text[len(name.text)-2:len(name.text)])
                    profile_url = profile.get_attribute("href")
                    age_profile_dict[profile_url] = age
                except Exception:
                    pass
            self.logger.log("Found ages = " + str(age_profile_dict))
            return age_profile_dict
        except Exception:
            raise TestFailedException("Failed to get users age list")

    def get_users_amount(self):
#        get users profile and users list in a single dictionary
        return len(self.get_elements_by_xpath(self._user_items_xpath))

    def get_users_xpath(self):
        return self._user_items_xpath

    def get_user_online_xpath(self):
        return self._user_online_icon_xpath

    def get_user_goal_xpath(self,goal):
        return self._user_goal_beginning_xpath + str(goal) + "')]"

    def get_user_profile(self,user_xpath):
        return self.get_element_by_xpath(user_xpath + self._user_profile_link_xpath).get_attribute("href")


