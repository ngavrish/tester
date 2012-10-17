from engine.test_failed_exception import TestFailedException
from topface.model.object_model import ObjectModel

__author__ = 'ngavrish'

class Energy(ObjectModel):

    _energy_profile_xpath = ".//*[@id='sideMenu']//div[contains(@class,'val')]"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def get_profile_percent_value(self):
        self.logger.log("Get profile energy value")
        try:
            return float(self.browser.find_element_by_xpath(".//*[@id='sideMenu']//div[contains(@class,'val')]")\
                                    .get_attribute("innerHTML")[:-1].replace(",", "."))
        except Exception:
            raise TestFailedException("Failed to get profile energy float value")


    def get_colour(self):
        pass

    def get_buy_energy_popup(self):
        pass

