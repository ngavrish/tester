# coding=utf-8
from topface.model.custom_objects.auth import AuthForm
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.object_model import ObjectModel
from topface.model.custom_objects.navigation import Navigation

__author__ = 'ngavrish'

class Profile(ObjectModel):
    marks_after_reset_amount = 5
    boundary_marks_amount = 30
    _display_bock_style = "display: block;"
#   PROFILE VIEW
    _online_status_class = "onlineOnPhoto"

    _online_indicator = "//div[@id='onlineStatus']"
    _top_default_status_xpath = "//div[@id='statusTopBalloon']//span[contains(text(),'Я ищу парня, 67-75, Москва')]"
    _avatar_default_photo_xpath = "//div[@id='userPhotoLayout']//*[@src='http://profile.ak.fbcdn.net/static-ak/rsrc.php/v2/yL/r/HsTZSDw4avx.gif']"
    _profile_view_name_container_xpath = "//div[@class='name-container']/h1[contains(text(),'"
    _profile_view_age_and_place_xpath = "//div[@class='name-container' and contains(text(),'"
    _photo_preview_bar_xpath = "//div[@id='photoalbumLayout']//div[@class='photos-container']"
    _photo_preview_prev_button_xpath = "//div[@id='photoalbumLayout']/a[@class='prev-arrow']"
    _photo_preview_next_button_xpath = "//div[@id='photoalbumLayout']/a[@class='next-arrow']"
    _photo_preview_add_photo_button_xpath = "//a[contains(@class,'button') and contains(text(),'" + \
                                            u"Добавить фото" + "')]"
    _anketa_box_xpath = "//div[contains(@class,'questionary-answers')]"
    _presents_box_xpath = "//div[@id='profile-gifts']"
    _badges_box_xpath = "//div[@id='achieved-badges']"
    _board_feed_xpath = "//div[@id='boardFeed']"
#    SETTINGS VIEW
    _form_name_settings_id = "form_settings_first_name"
    _form_sex_settings_id = "form_settings_sex"
    _form_age_settings_id = "form_settings_age"
    _form_lang_settings_id = "form_settings_lang"
    _form_city_settings_id = "cityAc"
    _form_user_wish_status_id = "form_settings_userWishStatus"
    _form_user_name_translit_id = "form_settings_name_translit"
    _form_status_short_id = "form_settings_short"
    _form_my_friends_see_me_settings_id = "form_settings_my_friends_see_me"
    _form_disable_sound_settings_id = "form_settings_disable_sound"
    _form_hide_social_profile_settings_id = "form_settings_hide_social_profile"
    _save_setting_button_id = "save-settings"
#   NOTIFICATIONS
    _form_mail_board_settings_id = "form_settings_mail_board"
    _form_mail_gifts_settings_id = "form_settings_mail_gifts"
    _form_mail_themegifts_settings_id = "form_settings_mail_themegifts"
    _form_mail_photocomments_settings_id = "form_settings_mail_photocomments"
    _form_mail_rates_settings_id = "form_settings_mail_rates"
    _form_mail_ratesmax_settings_id = "form_settings_mail_ratesmax"
    _form_mail_visitors_settings_id = "form_settings_mail_visitors"
    _form_mail_newmessages_settings_id = "form_settings_mail_newmessages"
    _form_mail_wishes_settings_id = "form_settings_mail_wishes"
    _form_interval_O_settings_id = "form_settings_interval_0"
    _form_interval_1_settings_id = "form_settings_interval_1"
    _form_interval_3_settings_id = "form_settings_interval_3"
    _form_interval_7_settings_id = "form_settings_interval_7"
    _form_interval_never_settings_id = "form_settings_interval_-1"
#    CONTACTS
    _contacts_help_description_id = "Help"
#   PHOTO
    _photo_add_new_button_id = "addNewPhotoButton"
    _photo_main_tip_xpath = "//div[@id='photo-items']//span[@class='main-photo-tip']"
    _photo_main_rating_xpath = "//div[@id='photo-items']//div[@class='myalbum-info']//div[@class='with-rating']"
    _photo_main_rating_rates_amount_xpath = "//div[@id='photo-items']//div[@class='myalbum-info']//div[@class='with-rating']//span/b"
    _photo_main_need_rates_xpath = "//div[@id='photo-items']//div[@class='myalbum-info']//div[@class='need-rates']"
    _photo_main_reset_rating_wrapper_xpath = "//div[@id='photo-items']//div[@class='myalbum-info']//div[text()='Понравилось']"
    _photo_main_reset_rating_link_xpath = "//div[@id='photo-items']//div[@class='myalbum-info']//div[text()='Понравилось']/a"
    _photo_main_empty_rate_percentage_xpath = "//div[@id='photo-items']//div[@class='myalbum-info']//div[@class='with-rating']/span[not(contains(text(),'%'))]"
    _photo_my_album_image_xpath = "//div[@id='photo-items']//div[@class='myalbum-image']//img"
    _photo_add_photo_title_xpath = "//div[@id='photo-items']//a[@class='add-photo-title']"
    _photo_title_input_active_xpath = "//div[@id='photo-items']//div[@class='toggle-comment' and @style!='display: none']//input"
    _photo_get_album_text_xpath = "//div[@class='myalbum_text']"
    _photo_album_get_more_info_id = "getMoreInfo"
    _photo_album_text_more_id = "album_text_more"

    def __init__(self, browser, logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def validate_profile_view(self,user=None):
        auth = AuthForm(self.browser,self.logger)

        if user is None:
            user = auth.User1
#        validate default status message
        try:
            self.wait4xpath(settings.wait_for_element_time, self._top_default_status_xpath)
            assert self.get_element_by_xpath(self._online_indicator).get_attribute('class') == self._online_status_class
        except AssertionError:
            raise TestFailedException("Failed to validate status")
        try:
    #        validate default image
            self.wait4xpath(settings.wait_for_element_time,self._avatar_default_photo_xpath)
    #        validate name
            self.wait4xpath(settings.wait_for_element_time,
                            self._profile_view_name_container_xpath + user.fb_human_name + "')]")
    #        validate age
            self.wait4xpath(settings.wait_for_element_time,
                            self._profile_view_age_and_place_xpath + user.fb_human_age + "')]")
    #        validate place
            self.wait4xpath(settings.wait_for_element_time,
                self._profile_view_age_and_place_xpath + user.fb_human_place + "')]")
    #        validate photo preview bar
            self.wait4xpath(settings.wait_for_element_time,
                            self._photo_preview_bar_xpath)
            self.wait4xpath(settings.wait_for_element_time,
                            self._photo_preview_next_button_xpath)
            self.wait4xpath(settings.wait_for_element_time,
                            self._photo_preview_prev_button_xpath)
            self.wait4xpath(settings.wait_for_element_time,
                            self._photo_preview_add_photo_button_xpath)
    #    validate anketa
            self.wait4xpath(settings.wait_for_element_time,
                            self._anketa_box_xpath)
    #    validate presents
            self.wait4xpath(settings.wait_for_element_time,
                            self._presents_box_xpath)
    #        validate badges
            self.wait4xpath(settings.wait_for_element_time,
                            self._badges_box_xpath)
    #       validate wall board
            self.wait4xpath(settings.wait_for_element_time,
                            self._board_feed_xpath)
        except Exception as e:
            raise TestFailedException("Failed to validate profile view: " + e.message)

    def validate_notifications_view(self):
        try:
            self.wait4id(settings.wait_for_element_time,self._form_mail_board_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_mail_gifts_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_mail_themegifts_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_mail_photocomments_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_mail_rates_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_mail_ratesmax_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_mail_visitors_settings_id)
            self.wait4id(settings.wait_for_element_time, self._form_mail_newmessages_settings_id)
            self.wait4id(settings.wait_for_element_time, self._form_mail_wishes_settings_id)
            self.wait4id(settings.wait_for_element_time, self._form_interval_O_settings_id)
            self.wait4id(settings.wait_for_element_time, self._form_interval_1_settings_id)
            self.wait4id(settings.wait_for_element_time, self._form_interval_3_settings_id)
            self.wait4id(settings.wait_for_element_time, self._form_interval_7_settings_id)
            self.wait4id(settings.wait_for_element_time, self._form_interval_never_settings_id)
        except Exception as e:
            raise TestFailedException("Failed to validate notifications view: " + e.message)

    def validate_settings_view(self):
        try:
            self.wait4id(settings.wait_for_element_time,self._form_name_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_sex_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_age_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_lang_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_city_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_user_wish_status_id)
            self.wait4id(settings.wait_for_element_time,self._form_user_name_translit_id)
            self.wait4id(settings.wait_for_element_time,self._form_status_short_id)
            self.wait4id(settings.wait_for_element_time,self._form_my_friends_see_me_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_disable_sound_settings_id)
            self.wait4id(settings.wait_for_element_time,self._form_hide_social_profile_settings_id)
        except Exception as e:
            raise TestFailedException("Failed to validate settings view: " + e.message)

    def validate_contacts_view(self):
        try:
            self.wait4id(settings.wait_for_element_time,self._contacts_help_description_id)
        except Exception as e:
            raise TestFailedException("Failed to validate contacts view: " + e.message)

    def validate_photo_view(self):
        try:
            self.wait4id(settings.wait_for_element_time,self._photo_add_new_button_id)
            self.wait4xpath(settings.wait_for_element_time,self._photo_main_tip_xpath)
            self.wait4xpath(settings.wait_for_element_time,self._photo_main_rating_xpath)
#            validate if too litle of rates
            if int(self.wait4xpath(settings.wait_for_element_time,self._photo_main_rating_rates_amount_xpath).text) <\
               self.boundary_marks_amount:
#                marks are not enough
                self.wait4xpath(settings.wait_for_element_time,self._photo_main_need_rates_xpath)
            else:
                self.wait4xpath(settings.wait_for_element_time,self._photo_main_reset_rating_wrapper_xpath)
#           reset rating
                self.click(
                    self.wait4xpath(settings.wait_for_element_time,self._photo_main_reset_rating_link_xpath))
                try:
                    self.wait4xpath(settings.wait_for_element_time,self._photo_main_reset_rating_wrapper_xpath)
                    raise TestFailedException("Reset wrapper exists but shouldn't")
                except TestFailedException:
                    raise
                except Exception:
                    print "Reset wrapper doesn't exist and that is how it should be"
                    self.wait4xpath(settings.wait_for_element_time,self._photo_main_rating_xpath)
                self.wait4xpath(settings.wait_for_element_time,self._photo_main_empty_rate_percentage_xpath)
            self.wait4xpath(settings.wait_for_element_time,self._photo_my_album_image_xpath)
            self.click(
                self.wait4xpath(settings.wait_for_element_time,self._photo_add_photo_title_xpath))
            self.wait4xpath(settings.wait_for_element_time,self._photo_title_input_active_xpath)
            self.wait4xpath(settings.wait_for_element_time,self._photo_get_album_text_xpath)
            self.click(
                self.wait4id(settings.wait_for_element_time,self._photo_album_get_more_info_id))
            try:
                assert self.wait4id(settings.wait_for_element_time,self._photo_album_text_more_id).\
                            get_attribute("style") == self._display_bock_style
            except AssertionError as e:
                raise TestFailedException("Failed to expand more photo album text: " + e.message)
        except Exception as e:
            raise TestFailedException("Failed to validate photo view: " + e.message)
        print "No validation implemented"

    def validate_horo_view(self):
        print "No validation implemented"

    def set_age(self,age):
        navigation = Navigation(self.browser,self.logger)

        navigation.goto_top_menu_item(u"Профиль")
        navigation.goto_tab_menu_item(u"Настройки")
        self.enter_text(
            self.get_element_by_id(self._form_age_settings_id),
            age)
        self.click(
            self.get_element_by_id(self._save_setting_button_id))