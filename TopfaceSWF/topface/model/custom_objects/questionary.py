# coding=utf-8
from time import sleep
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.object_model import ObjectModel

__author__ = 'ngavrish'

class Questionary(ObjectModel):
    _valid_data_message = u"Спасибо за внесение изменений в вашу анкету."
    _not_enough_answers_message = u"Вам необходимо ответить минимум на"
    _fix_errors_message = u"Пожалуйста исправьте ошибки"
    _sample_text = u"Блаблабла"
    _empty_string = ""
    _first_valuable_select_value = "2"
    _nothing_selected_value = "0"
    _custom_option_value = "1"
    _sample_number_value = 146

    _edit_show_link_xpath = "//a[@class='edit-questionary' and contains(text(),'" + u"Редактировать" + "')]"
    _edit_hide_link_xpath = "//a[@class='edit-questionary' and contains(text(),'" + u"Закрыть" + "')]"
    _questionary_wrapper_xpath = "//div[@class='questionary-toggle']"
# ============= FIRST 13 SAVED =================
    _about_yourself_text_id = "form_questionary_about"
    _hide_birthday_id = "form_questionary_hide_birthday"
    _hide_university_id = "form_questionary_hide_university"
    _job_drop_down_id = "form_questionary_job"
    _job_input_id = "questionary_job_input"
    _job_close_btn_xpath = ".//*[@id='questionary_job_input']/div[contains(@class,'close-btn-round')]"
    _questionary_status_dropdown_id = "form_questionary_status"
    _questionary_status_input_id = "questionary_status_input"
    _questionary_status_close_btn_xpath = ".//*[@id='questionary_status_input']/div[contains(@class,'close-btn-round')]"
    _height_id = "form_questionary_height"
    _weight_id = "form_questionary_weight"
    _marriage_dropdown_id = "form_questionary_marriage"
    _children_dropdown_id = "form_questionary_children"
    _education_dropdown_id = "form_questionary_education"
    _finance_dropdown_id = "form_questionary_finances"
    _communication_dropdown_id = "form_questionary_communication"
    _character_dropdown_id = "form_questionary_character"
    _smoking_dropdown_id = "form_questionary_smoking"
    _alcohol_dropdown_id = "form_questionary_alcohol"
    _fitness_dropdown_id = "form_questionary_fitness"
#    ============= END OF 1ST 13 SAVED =================
    _haircolor_dropdown_id = "form_questionary_hairColor"
    _eyecolor_dropdown_id = "form_questionary_eyeColor"
    _residence_dropdown_id = "form_questionary_residence"
    _hascar_dropdown_id = "form_questionary_hasCar"
    _restaurants_text_id = "form_questionary_restaurants"
    _firstdate_text_id = "form_questionary_firstDate"
    _achievement_text_id = "form_questionary_achievement"
    _valuables_text_id = "form_questionary_valuables"
    _aspirations_text_id = "form_questionary_aspirations"
    _australia_checkbox_xpath = "//div[contains(@class,'checkbox-set visited-countries')]//label[1]/input"

    _countries_checkboxes_xpath = "//div[contains(@class,'checkbox-set visited-countries')]//input"
    _countries_error_xpath = "//div[@class='checkbox-set visited-countries err']"
    _savesettings_button_xpath = "//a[contains(@class,'saveSettings')]"
    _cancelsettings_link_xpath = "//a[contains(@class,'cancel-button')]"
    _onsave_message_id = "questionary_msg"


    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def __get_country_checkbox_xpath(self,country_name):
        return "//div[contains(@class,'checkbox-set visited-countries')]//label[text()='"\
           + country_name + "']//input"

    def expand(self):
        self.logger.log("Expand questionary for editing")
        try:
            self.click(
                self.wait4xpath(settings.wait_for_element_time,self._edit_show_link_xpath))
            try:
                assert self.wait4xpath(settings.wait_for_element_time,
                        self._questionary_wrapper_xpath).is_displayed()
            except AssertionError as e:
                raise TestFailedException("Questionary wrapper style haven't been changed: " + e.message)
        except Exception as e:
            raise TestFailedException("Failed to expand edit wrapper: " + e.message)

    def hide(self):
        self.logger.log("Hide questionary for editing")
        try:
            self.click(
                self.wait4xpath(settings.wait_for_element_time,self._edit_hide_link_xpath))
            try:
                assert not self.wait4xpath(settings.wait_for_element_time,
                        self._questionary_wrapper_xpath).is_displayed()
            except AssertionError as e:
                raise TestFailedException("Questionary wrapper failed to collapse: " + e.message)
        except Exception as e:
            raise TestFailedException("Failed to hide questionary: " + e.message)

    def cancel(self):
        self.logger.log("Cancel saving questionary")
        try:
            self.click(
                self.wait4xpath(settings.wait_for_element_time,self._cancelsettings_link_xpath))
            try:
                assert not self.wait4xpath(settings.wait_for_element_time,
                        self._questionary_wrapper_xpath).is_displayed()
            except AssertionError as e:
                raise TestFailedException("Questionary wrapper failed to collapse: " + e.message)
        except Exception as e:
            raise TestFailedException("Failed to hide questionary: " + e.message)

    def click_country_checkbox(self,country_name):
        self.logger.log("Select/Deselect " + country_name)
        try:
            self.click(
                self.wait4xpath(settings.wait_for_element_time,self.__get_country_checkbox_xpath(country_name)))
        except Exception as e:
            TestFailedException("Failed to check/uncheck " + country_name + ": " + e.message)

    def uncheck_all_countries(self):
        self.logger.log("Uncheck all countries")
        countries_checkboxes = self.wait4xpath_s(settings.wait_for_element_time,self._countries_checkboxes_xpath)
        for checkbox in countries_checkboxes:
            if checkbox.get_attribute("checked") == "true":
                self.click(checkbox)

    def save(self):
        self.logger.log("Saving settings with no countries selected")
        try:
            self.click(
                self.wait4xpath(settings.wait_for_element_time,self._savesettings_button_xpath))
        except Exception:
            TestFailedException("Failed to perform saving questionary with no countries selected correctly")

    def fill_first_14_elements(self):
        try:
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._job_drop_down_id),self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._questionary_status_dropdown_id),self._first_valuable_select_value)
            self.enter_text(
                self.get_element_by_id(self._height_id),self._sample_number_value)
            self.enter_text(
                self.get_element_by_id(self._weight_id),self._sample_number_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._marriage_dropdown_id),self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._children_dropdown_id),self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._education_dropdown_id),self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._finance_dropdown_id),self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._communication_dropdown_id), self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._character_dropdown_id), self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._smoking_dropdown_id), self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._alcohol_dropdown_id), self._first_valuable_select_value)
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._fitness_dropdown_id), self._first_valuable_select_value)
            self.click(
                self.get_element_by_xpath(self._australia_checkbox_xpath))
        except Exception as e:
            raise TestFailedException("Failed to fill question: " + e.message)

    def check_dropdowns_to_input_transformation(self):
        """
        Character and Job dropdown lists to input and backwards
        """
        try:
            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._questionary_status_dropdown_id),self._custom_option_value)
            self.wait4id(settings.wait_for_element_time,self._questionary_status_input_id)
            self.click(
                self.wait4xpath(settings.wait_for_element_time,self._questionary_status_close_btn_xpath))
            try:
                assert not self.wait4id(settings.wait_for_element_time,self._questionary_status_input_id).is_displayed()
            except AssertionError:
                raise TestFailedException("Failed to return back to select dropdown")

            self.select_from_dropdown_by_value(
                self.get_element_by_id(self._job_drop_down_id),self._custom_option_value)
            self.wait4id(settings.wait_for_element_time,self._questionary_status_input_id)
            self.click(
                self.wait4xpath(settings.wait_for_element_time,self._job_close_btn_xpath))
            try:
                assert not self.wait4id(settings.wait_for_element_time,self._job_input_id).is_displayed()
            except AssertionError:
                raise TestFailedException("Failed to return back to select dropdown")
        except Exception:
            raise TestFailedException("Failed to validate transformation from normal select to input or backwards")

    def fill_all(self):
        self.fill_first_14_elements()
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._haircolor_dropdown_id),self._first_valuable_select_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._eyecolor_dropdown_id),self._first_valuable_select_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._residence_dropdown_id),self._first_valuable_select_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._hascar_dropdown_id),self._first_valuable_select_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._residence_dropdown_id),self._first_valuable_select_value)
        self.enter_text(
            self.get_element_by_id(self._firstdate_text_id),self._sample_text)
        self.enter_text(
            self.get_element_by_id(self._achievement_text_id),self._sample_text)
        self.enter_text(
            self.get_element_by_id(self._valuables_text_id),self._sample_text)
        self.enter_text(
            self.get_element_by_id(self._aspirations_text_id),self._sample_text)
        self.click(
            self.get_element_by_xpath(self._australia_checkbox_xpath))

    def unfill_all(self):
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._job_drop_down_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._questionary_status_dropdown_id),self._nothing_selected_value)
        self.enter_text(
            self.get_element_by_id(self._height_id),self._empty_string)
        self.enter_text(
            self.get_element_by_id(self._weight_id),self._empty_string)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._marriage_dropdown_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._children_dropdown_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._education_dropdown_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._finance_dropdown_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._communication_dropdown_id), self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._character_dropdown_id), self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._smoking_dropdown_id), self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._alcohol_dropdown_id), self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._fitness_dropdown_id), self._nothing_selected_value)

        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._haircolor_dropdown_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._eyecolor_dropdown_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._residence_dropdown_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._hascar_dropdown_id),self._nothing_selected_value)
        self.select_from_dropdown_by_value(
            self.get_element_by_id(self._residence_dropdown_id),self._nothing_selected_value)
        self.enter_text(
            self.get_element_by_id(self._firstdate_text_id),self._empty_string)
        self.enter_text(
            self.get_element_by_id(self._achievement_text_id),self._empty_string)
        self.enter_text(
            self.get_element_by_id(self._valuables_text_id),self._empty_string)
        self.enter_text(
            self.get_element_by_id(self._aspirations_text_id),self._empty_string)

    def validate_filled_all(self):
        questionary_dropdown_answers = [
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._job_drop_down_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._questionary_status_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._marriage_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._children_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._education_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._finance_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._communication_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._character_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._smoking_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._alcohol_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._fitness_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._haircolor_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._eyecolor_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._residence_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._hascar_dropdown_id)),
            self.get_selected_value_from_dropdown(
                self.get_element_by_id(self._residence_dropdown_id)),
            ]

        questionary_text_answers = [
            self.get_element_by_id(self._firstdate_text_id).text,
            self.get_element_by_id(self._achievement_text_id).text,
            self.get_element_by_id(self._valuables_text_id).text,
            self.get_element_by_id(self._aspirations_text_id).text,
            self.get_element_by_id(self._height_id).get_attribute("value"),
            self.get_element_by_id(self._weight_id).get_attribute("value")
        ]

        if self._nothing_selected_value in questionary_dropdown_answers:
            raise TestFailedException("Failed to validate filled answers in dropdowns")

        if self._empty_string in questionary_text_answers:
            raise TestFailedException("Failed to validate filled answers in inputs")



    def validate_error_msg_wrong_data(self):
        try:
            self.wait4xpath(settings.wait_for_element_time,self._countries_error_xpath)
        except Exception:
            self.logger.log("No countries error found")
        try:
            assert self.wait4id(settings.wait_for_element_time,self._onsave_message_id).text ==\
                   self._fix_errors_message
        except AssertionError as e1:
            raise TestFailedException("Failed to get message about fixing errors: " +
                                      self._fix_errors_message + ": " + e1.message)

    def validate_error_msg_answers_not_enough(self):
#        need to wait for some time before element text will be changed
        sleep(10)
        if self._valid_data_message not in self.get_element_by_id(self._onsave_message_id).get_attribute("innerHTML")\
            or\
            self._not_enough_answers_message not in self.get_element_by_id(self._onsave_message_id).get_attribute("innerHTML"):
            raise TestFailedException("Failed to validate message about low number of answered questions")

    def validate_saved_correctly(self):
        try:
            assert self._valid_data_message in self.get_element_by_id(self._onsave_message_id).get_attribute("innerHTML")
        except Exception:
            raise TestFailedException("Failed to validate correct questionary saving")

    def get_questionary_value_by_description(self,descr):
        self.logger.log("Getting value from questionary by description = " + str(descr))
        return self.get_element_by_xpath("//div[contains(@class,'questionary-answers')]//td[@class='questionary-title' "
                                         "and contains(text(),'" + descr + "')]/../td[2]").text