# coding=utf-8
from engine.test_failed_exception import TestFailedException
import settings
from topface.model.object_model import ObjectModel

__author__ = 'ngavrish'

class VIPPopups(ObjectModel):

    _premium_close_xpath = "//div[@role='dialog' and contains(@style,'display: block')]//span[text()='Премиум функция']/../a[@role='button']"
    _title_value = u"VIP функция"
    _title_id = "ui-dialog-title-dialog1"
    _illustration_fans_xpath = "//div[@id='dialog1']//i[contains(@class,'fans')]"
    _illustration_guests_xpath = "//div[@id='dialog1']//i[contains(@class,'guests')]"
    _vip_description_xpath = "//div[@id='dialog1']//p[1]"
    _vip_moreabout_vip_xpath = "//div[@id='dialog1']//p/a"
#    _buy_button_xpath = "//ul[@id='options']//span[text()='" + u"Купить" + "']"
    _buy_one_day_xpath = u"//ul[@id='options']//span[contains(text(),'1')]/../..//div[contains(text(),'0')]"
    _buy_seven_days_xpath = u"//ul[@id='options']//span[contains(text(),'7')]/../..//div[contains(text(),'0')]"
    _buy_month_xpath = u"//ul[@id='options']//span[contains(text(),'30')]/../..//div[contains(text(),'0')]"
    _get_free_button_xpath = "//div[text()='" + u"Получить бесплатно" + "']"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def close_premium(self):
        self.logger.log("Closing premium popup")
        self.click(
            self.get_element_by_xpath(self._premium_close_xpath))

    def validate_forbidden_nonvip(self):
        try:
            print self.wait4id(settings.wait_for_element_time,self._title_id).text + " vs " + self._title_value
            assert self.wait4id(settings.wait_for_element_time,self._title_id).text == self._title_value
        except AssertionError as e:
            raise TestFailedException("Failed to validate popup title: " + e.message)
        try:
            try:
                self.wait4xpath(settings.wait_for_element_time,self._illustration_fans_xpath)
            except Exception:
                try:
                    self.wait4xpath(settings.wait_for_element_time,self._illustration_guests_xpath)
                except Exception:
                    raise TestFailedException("Failed to validate")
            self.wait4xpath(settings.wait_for_element_time,self._vip_description_xpath)
            self.wait4xpath(settings.wait_for_element_time,self._vip_moreabout_vip_xpath)
            self.wait4xpath(settings.wait_for_element_time,self._buy_one_day_xpath)
            self.wait4xpath(settings.wait_for_element_time,self._buy_seven_days_xpath)
            self.wait4xpath(settings.wait_for_element_time,self._buy_month_xpath)
            self.wait4xpath(settings.wait_for_element_time,self._get_free_button_xpath)
        except Exception as e:
            raise TestFailedException("Failed to validate fans popup: " + e.message)
