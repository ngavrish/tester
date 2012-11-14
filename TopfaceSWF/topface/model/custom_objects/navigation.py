# coding=utf-8
from topface.model.object_model import ObjectModel
from topface.model.custom_objects.browser_window import BrowserWindow
from engine.test_failed_exception import TestFailedException
import settings


__author__ = 'ngavrish'

class Navigation(ObjectModel):

    _to_messenger_from_profile_id = "switch-message"
    _comments_wrapper_id = "comments"
    _side_menu_xpath = "//div[@id='sideMenu']//span[text()='"
    _top_main_menu_xpath = "//div[contains(@class,'top-menu')]//span[text()='"
    _top_active_main_menu_xpath = "//div[contains(@class,'top-menu')]//a[contains(@class,'active')]//span[text()='"
    _top_menu_xpath = "//div[contains(@class,'top-menu')]//span[text()='"
    _feed_tab_notext_xpath = "//div[@class='sub-menu']//a[text()='"
    _feed_active_tab_notext_xpath = "//div[@class='sub-menu']//a[contains(@class,'active') and text()='"
    _logo_xpath = "//a[@class='logotype']"
    _profile_name_link_id = "userName"
    _profile_photo_link_xpath = "//div[@id='userPhotoLayout']/div[@class='img']/a/img"
    _search_div_id = "searchList"

    def __init__(self, browser, logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def validate_in_search(self):
        self.logger.log("Validating search wrapper")
        self.wait4id(settings.wait_for_element_time,self._search_div_id)

    def get_profile_name_link(self):
        return self.get_element_by_id(self._profile_name_link_id)

    def get_profile_photo_link(self):
        return self.get_element_by_xpath(self._profile_photo_link_xpath)

    def goto_side_menu_item(self,text):
        self.logger.log("Getting side menu link by text = " + text)
        try:
            self.click(
                self.get_element_by_xpath(
                    self._side_menu_xpath + text + "']"))
        except Exception:
            raise TestFailedException("Failed to get mennu item with text = " + text)
        try:
            self.wait4id(settings.wait_for_element_time,self._comments_wrapper_id)
        except Exception:
            raise TestFailedException("Failed to navigate to feeds")
# Main horizontal menu
    def goto_main_top_menu_item(self,text):
        self.logger.log("Going to main horizontal menu item = " + text)
        try:
            self.click(
                self.get_element_by_xpath(
                    self._top_main_menu_xpath + text + "']"))
        except Exception:
            raise TestFailedException("Failed to get main menu item with text = " + text)
        self.validate_in_main_tab(text)

# Horizontal submenu
    def goto_top_menu_item(self,text):
        self.logger.log("Getting top menu link by text = " + text)
        try:
            self.click(
                self.get_element_by_xpath(
                    self._top_menu_xpath + text + "']"))
        except Exception:
            raise TestFailedException("Failed to get menu item with text = " + text)
        self.validate_in_tab(text)

    def goto_messenger_from_profile(self):
        try:
            window = BrowserWindow(self.browser,self.logger)
            self.logger.log("Going to messenger from profile")
            self.click(
                self.get_element_by_id(
                    self._to_messenger_from_profile_id))
            window.switch_to_popup()
            print self.browser.title
        except Exception:
            raise TestFailedException("Failed to validate navigation to messanger from profile")

    def goto_messenger_from_mutual_likes(self,user_profile):
        try:
            window = BrowserWindow(self.browser,self.logger)
            self.logger.log("Going to messenger from mutual likes")
            self.click(
                self.get_element_by_xpath(
                    "//div[@id='comments']//div[@class='comment-avatar-new']//a[@href='" + user_profile +
                    "']/../../div[@class='additional-actions']/a[@class='openHistory']"
                ))
            window.switch_to_popup()
            self.logger.log(self.browser.title)
        except Exception:
            raise TestFailedException("Failed to get to messenger from mutual likes")

    def goto_tab_menu_item(self,tab_name):
        self.logger.log("Navigating to " + tab_name + " feed box")
        try:
            self.click(
                self.wait4xpath(
                    settings.wait_for_element_time,
                    self._feed_tab_notext_xpath + tab_name + "']"
                ))
            self.validate_in_tab(tab_name)
        except Exception:
            raise TestFailedException("Failed to navigate to tab = " + tab_name)

    def validate_in_tab(self,tab_name):
        self.logger.log("Validate located to tab with name = " + tab_name)
        try:
            self.wait4xpath(settings.wait_for_element_time,self._feed_active_tab_notext_xpath + tab_name + "']")
        except Exception:
            raise TestFailedException("Failed to validate user in tab tabname = " + tab_name)

    def validate_in_main_tab(self,tab_name):
        self.logger.log("Validate located to main tab with name = " + tab_name)
        try:
            self.wait4xpath(settings.wait_for_element_time,self._top_active_main_menu_xpath + tab_name + "']")
        except Exception:
            raise TestFailedException("Failed to validate user in tab tabname = " + tab_name)

    def goto_main(self):
        self.logger.log("Navigate to main page via logo click")
        self.click(
            self.get_element_by_xpath(self._logo_xpath))

    def goto_profile_from_main(self,way="name"):
#        tow option available - name, photo
        if way == "name":
            self.click(
                self.get_element_by_id(self._profile_name_link_id))
        elif way == "photo":
            self.click(
                self.get_profile_photo_link())

