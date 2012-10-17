from selenium.common.exceptions import NoSuchElementException
from engine.test_failed_exception import TestFailedException
from topface.model.object_model import ObjectModel

__author__ = 'ngavrish'

class Filters(ObjectModel):

    _online_filter_checkbox_id = "onlineFilter"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def change_online_filter_value(self):
        self.logger.log("Changing online-filter status")
        try:
            self.click(
                self.get_element_by_id(
                    self._online_filter_checkbox_id
                )
            )
        except NoSuchElementException as e:
            raise TestFailedException("Failed to change online/offline filter status " + e.message)
