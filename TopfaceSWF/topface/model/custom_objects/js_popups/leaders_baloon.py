# coding=utf-8
from topface.model.object_model import ObjectModel

__author__ = 'pretender-test'

class LeadersBaloon(ObjectModel):

    _close_xpath = "//div[@class='leadersTopBalloon']//a[@class='close']"
    _close_fast_meet_xpath = u"//div[@class='leadersTopBalloon']/b[text()='Хочешь быстро познакомиться?']/../a[@class='close']"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def close(self):
        try:
            self.click(
                self.get_element_by_xpath(self._close_xpath))
        except Exception as e:
            print "No leaders baloon found"

    def close_want_fast_meet(self):
        try:
            self.click(
                self.get_element_by_xpath(self._close_fast_meet_xpath))
        except Exception as e:
            print "No want to meet fast baloon found"
