# coding=utf-8
from __future__ import division
import datetime
from time import sleep
import math
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.custom_objects.buttons import Buttons
from topface.model.custom_objects.comments import Comments
from topface.model.custom_objects.navigation import Navigation
from topface.model.custom_objects.js_popups.alert_popups import AlertPopups
from topface.model.object_model import ObjectModel

__author__ = 'ngavrish'

class Marks(ObjectModel):

    custom_top_mark_message_treshold = 2
    unique_amount = 1000
    _star_box_id = "starBox"
    _mark_sent_confirmation_message_xpath = ".//*[@id='starBox']/div[@class='rate-sent-notice']"
    _minor_marks_xpath = ".//*[@id='starBox']//a[@data-index!='0' "\
                         "and @data-index!='9' and @data-index!='10']"
    _major_marks_xpath = ".//*[@id='starBox']//a[@data-index='9' or @data-index='10']"
    _photo2mark_xpath = "//div[@id='userPhotoLayout']//a"
    _random_compliments_xpath = ".//*[@id='extraQuestions']//div[@class='questions-list']//label[contains(@class,'message-variant random-compliments')]"
    _marks_left_till_plus_xpath = "//div[@id='user-rates-bonus-block']//span[@class='power-bonus-message']"
    _comments_rate_bar_xpath = ".//*[@id='comments']//div[@class='commentRateBar']"
    _feed_profile_links_xpath = "//div[@id='comments']//div[@class='comment-avatar-new']//a"
    _feed_click4more_xpath = "//div[@id='comments']//a[@class='show-more icon-expand']"
    _fb_popup_close_link_xpath = "//a[@class='fb_dialog_close_icon']"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def _get_last_writeback_link_xpath(self,profile):
        return "//div[@class='feed-name-new']//a[@href='"\
                + profile +\
                "']/../../../../../../div[1]//div[@class='additional-actions']//a[@class='openHistory']"

    def _get_last_rateback_link_xpath(self,profile):
        return "//div[@class='feed-name-new']//a[@href='"\
               + profile +\
               "']/../../../../../../div[1]//div[@class='additional-actions']//a[@class='rate-answer']"

    def star_box(self):
        self.logger.log("Waiting for element with ID = " + self._star_box_id)
        try:
            return WebDriverWait(self.browser, settings.wait_for_element_time).\
            until(lambda driver: driver.find_element_by_id(self._star_box_id))
        except Exception:
            raise TestFailedException("Failed to get STARBOX - the marks wrapper")

    def get_minor_marks(self):
        self.logger.log("Get all minor marks - marks from 1 to 8")
        try:
            return WebDriverWait(self.browser,settings.wait_for_element_time).\
            until(lambda driver: driver.find_elements_by_xpath(self._minor_marks_xpath))
        except Exception:
            raise TestFailedException("Failed to get minor marks")

    def get_major_marks(self):
        self.logger.log("Getting major marks - marks from 9 to 10")
        try:
            return WebDriverWait(self.browser,settings.wait_for_element_time).\
            until(lambda driver: driver.find_elements_by_xpath(self._major_marks_xpath))
        except Exception:
            raise TestFailedException("Failed to get major marks")

    def get_mark_by_value(self,value):
        self.logger.log("Getting mark with value = " + str(value))
        try:
            return WebDriverWait(self.browser,settings.wait_for_element_time).\
            until(lambda driver: driver.find_element_by_xpath(".//*[@id='starBox']//a[@data-index='"+str(value)+"']"))
        except Exception:
            raise TestFailedException("Failed to get Mark by value = .//*[@id='starBox']//a[@data-index='"+str(value)+"']")

    def get_photo2mark_href(self):
        self.logger.log("Get photo to mark")
        try:
            sleep(2)
            return WebDriverWait(self.browser,settings.wait_for_element_time).\
                until(lambda driver: driver.find_element_by_xpath(self._photo2mark_xpath).get_attribute("href"))
        except Exception:
            raise TestFailedException("Failed to get photo href to mark")

    def get_random_compliments(self):
        self.logger.log("Getting random compliments elements")
        try:
            return  WebDriverWait(self.browser, settings.wait_for_element_time).\
            until(lambda driver: driver.find_elements_by_xpath(self._random_compliments_xpath))
        except Exception:
            raise TestFailedException("Failed to get random compliments elements")

    def get_marks_left_till_energy_plus(self):
        self.logger.log("Getting marks left till energy plus")
        try:
            return self.get_element_by_xpath(self._marks_left_till_plus_xpath).get_attribute("innerHTML")
        except Exception:
            raise TestFailedException("Failed to get marks till energy plus")

    def validate_profile_mark_sent(self):
        self.logger.log("Validating that UI has message that tells that message was sent")
        try:
            self.wait4xpath(settings.wait_for_element_time,self._mark_sent_confirmation_message_xpath)
        except Exception:
            raise TestFailedException("Failed to validate profile UI sent mark message")
        #        //div[@class='feed-name-new']//a[@href='http://topface.com/profile/41694213/']/../../../../../../div[1]//div[@class="date" and contains(text(),"29 Авг")]

    def get_comments_mark_by_value(self,value):
        try:
            return self.wait4xpath(settings.wait_for_element_time,
                                    self._comments_rate_bar_xpath + "//div[@class='starry']//a[@data-index='" + str(value) + "']")
        except Exception as e:
            raise TestFailedException("Failed to get comments mark " + str(value) +
                                      " exception details: " + e.message)

    def validate_new_mark_in_feed(self,profile_url,date=u"29 Авг"):
        try:
            self.wait4xpath(settings.wait_for_element_time,
                "//div[@class='feed-name-new']//a[@href='" + profile_url + "']")
            self.wait4xpath(settings.wait_for_element_time,
                "//div[@class='feed-name-new']//a[@href='" + profile_url +
                "']/../../../../../../div[1]//div[@class='date' and contains(text()," + date + ")]")
        except Exception:
            raise TestFailedException("Failed to validate profile UI sent mark message")

    def rate_answer(self,profile):
        try:
            open_rate_box_link = self.wait4xpath(settings.wait_for_element_time,
                self._get_last_rateback_link_xpath(profile))
            self.hover(open_rate_box_link)
            #            validate write from feed link is visible
            writeback_link = self.wait4xpath(settings.wait_for_element_time,
                self._get_last_writeback_link_xpath(profile))
            if writeback_link.get_attribute("style") == "display: inline;":
                raise TestFailedException("Writeback link failed to fadeIn")
            self.click(open_rate_box_link)
            rate_box = self.wait4xpath(settings.wait_for_element_time,
                self._comments_rate_bar_xpath)
            if rate_box.get_attribute("style") != "display: block;":
                raise TestFailedException("Ratebox failed to fadeIn")
            self.click(
                self.get_comments_mark_by_value(1)
            )
            rate_box = self.wait4xpath(settings.wait_for_element_time,
                self._comments_rate_bar_xpath)
            print rate_box.get_attribute("style")
            if rate_box.get_attribute("style") == "display: block;":
                raise TestFailedException("Ratebox failed to fadeOut")
        except Exception as e:
            raise TestFailedException("Failed to rate latest user " + profile + " answer: " +  e.message)

    def mark(self,value=2):
        """
        By default setting 2 mark
        """
        mark = self.get_mark_by_value(value)
        while mark.get_attribute("class").find("high_star") > 0:
            value -= 1
            if value == 0:
                raise TestFailedException("Failed to set mark. Only likes left")
            mark = self.get_mark_by_value(value)
        self.click(mark)


    def like(self,value=8):
        """
        By default setting 8 mark
        """
        mark = self.get_mark_by_value(value)
        while mark.get_attribute("class").find("high_star") < 0:
            value += 1
            if value == 9:
                raise TestFailedException("Failed to like user for free from main page")
            mark = self.get_mark_by_value(value)
        self.click(mark)

    def click(self, element):
        try:
            self.logger.log("Clicking on mark " + self.get_element_xpath(element))
            hover = ActionChains(self.browser).move_to_element(element)
            hover.perform()
            element.click()
        except Exception:
            raise TestFailedException("Failed to click on element " + self.get_element_xpath(element))

    def like_users_from_main(self,count):
        users_liked = []
        for i in range(count):
            photo_href1 = self.get_photo2mark_href()
            self.like()
            photo_href2 = self.get_photo2mark_href()
            if photo_href1 == photo_href2:
                raise TestFailedException("User haven't been changed after marking")
            users_liked.append(photo_href1)
            self.mark()
        return users_liked

    def get_mutual_profiles(self):
        """
        get user profiles list from feed 'Взаимно'
        """
        navigation = Navigation(self.browser,self.logger)
        navigation.goto_side_menu_item(u"Взаимно")
        has_more = True
        while has_more:
            try:
                click4more = self.wait4xpath(settings.wait_for_element_time,self._feed_click4more_xpath)
                click4more.click()
            except Exception as e:
                print "Couldn't find more on feed: " + e.message
                has_more = False
        if not has_more:
            mutual_users_links = self.wait4xpath_s(settings.wait_for_element_time,self._feed_profile_links_xpath)
            print "Mutual users links amount = " + str(len(mutual_users_links))
            output_profiles = []
            for user_link in mutual_users_links:
                output_profiles.append(user_link.get_attribute("href"))
            return output_profiles
        else:
            return None

    def get_answered_messages(self,auhors):
        navigation = Navigation(self.browser,self.logger)
        navigation.goto_side_menu_item(u"Сообщения")
        answered_users = []
        has_more = True
        while has_more:
            try:
                click4more = self.wait4xpath(settings.wait_for_element_time,self._feed_click4more_xpath)
                click4more.click()
            except Exception as e:
                print "Couldn't find more on feed: " + e.message
                has_more = False
        if not has_more:
            all_authors = self.wait4xpath_s(settings.wait_for_element_time,self._feed_profile_links_xpath)
            print "All messages amount = " + str(len(all_authors))
            self.logger.log("All messages amount = " + str(len(all_authors)))
            for user in auhors:
                if user in all_authors:
                    answered_users.append(user)
            return answered_users
        else:
            return None

    def mark_and_validate_mark(self,mark):
        photo_href1 = self.get_photo2mark_href()
        self.click(mark)
        photo_href2 = self.get_photo2mark_href()
        try:
            assert photo_href1 != photo_href2
        except AssertionError:
            raise TestFailedException("User haven't been changed after marking")

    def mark_major_marks_custom_comment(self,marks):
        error_count = 0
        comments = Comments(self.browser, self.logger)
        alerts = AlertPopups(self.browser, self.logger)
        for mark in marks:
            if error_count < self.custom_top_mark_message_treshold:
                photo_href1 = self.get_photo2mark_href()
                self.click(mark)
                top_mark_comment = comments.get_high_mark()
                comments.is_initial_top_mark_comment(top_mark_comment)
                if top_mark_comment.get_attribute("style") != "":
                    error_count += 1
                comments.click(top_mark_comment)
                #                reload comment element from web interface
                top_mark_comment = comments.get_high_mark()

                print top_mark_comment.get_attribute("style")

                if top_mark_comment.get_attribute("style").count(comments.get_top_mark_comment_height()) <= 0:
                    error_count += 1
                #                validate that comment textarea still contains initial text
                #                BUG NEXT LINE
                #                comments.is_initial_top_mark_comment(top_mark_comment)
                #                send single key
                comments.send_comment(top_mark_comment, u'1', "topmark")
                alerts.too_short_comment_close()
                comments.click(top_mark_comment)
                comments.send_comment(top_mark_comment, u"Привет", "topmark")
                photo_href2 = self.get_photo2mark_href()
                try:
                    assert photo_href1 != photo_href2
                except AssertionError:
                    raise TestFailedException("User haven't been changed after marking")
                try:
                    self.click(
                        self.get_element_by_xpath(self._fb_popup_close_link_xpath))
                except Exception:
                    self.logger.log("Fb Popup was not found")
            else:
                raise TestFailedException("User standart message failure. Error count >= " +
                                          str(self.custom_top_mark_message_treshold))

    def mark_major_marks_standart_comment(self,marks):
        comments = Comments(self.browser, self.logger)
        buttons = Buttons(self.browser, self.logger)

        for mark in marks:
            photo_href1 = self.get_photo2mark_href()
            self.click(mark)
            compliments = self.get_random_compliments()
            self.logger.log("Amount of compliments avaliable = " + str(len(compliments)))
            compliments_error_threshold = math.ceil(len(compliments)/2)
            self.logger.log("Compliments change error threshold = " + str(compliments_error_threshold))
            error_count = 0
            for compliment in compliments:
                self.click(compliment)
                sleep(3)
                try:
                    comments.validate_high_mark_comment_value(compliment.text)
                except Exception:
                    error_count += 1
                if error_count >= compliments_error_threshold:
                    raise TestFailedException("Faield standart comment sending functionality. " +\
                                              "Error count during sending comments = " + str(error_count))
            buttons.send_comment("topmark")
            photo_href2 = self.get_photo2mark_href()
            try:
                self.click(
                    self.get_element_by_xpath(self._fb_popup_close_link_xpath))
            except Exception:
                self.logger.log("Fb Popup was not found")
            try:
                print photo_href1
                print photo_href2
                assert photo_href1 != photo_href2
            except AssertionError:
                raise TestFailedException("User photo hasn't changed")

    def marking_made_closer_to_more_energy(self,i):
        mark_seven = self.get_mark_by_value(7)
        marks_left_till_plus = self.get_marks_left_till_energy_plus()
        marks_left_new_before_click = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
        self.click(mark_seven)
        marks_left_till_plus = self.get_marks_left_till_energy_plus()
        marks_left_new_after_click = [int(s) for s in marks_left_till_plus.split() if s.isdigit()][0]
        try:
            assert marks_left_new_after_click == (marks_left_new_before_click - 1)
        except AssertionError:
            raise TestFailedException("Click wrongly changed amount of left clicks on step " + str(i))

