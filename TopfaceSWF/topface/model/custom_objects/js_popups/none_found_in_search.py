# coding=utf-8
from topface.model.object_model import ObjectModel

__author__ = 'pretender-test'

class NoneFoundInSearch(ObjectModel):

    _close_xpath = "//div[@role='dialog' and contains(@style,'display: block')]//a[@role='button']"
    _close_mark_everyone_xpath = u"//div[@role='dialog' and contains(@style,'display: block')]//a[@class='button' and text()='Оценивать всех']"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def close(self):
        try:
            self.click(
                self.get_element_by_xpath(self._close_xpath))
        except Exception as e:
            print "No close xpath found"

    def mark_everyone(self):
        try:
            self.click(
                self.get_element_by_xpath(self._close_mark_everyone_xpath))
        except Exception as e:
            print "No mark everyone button found"
