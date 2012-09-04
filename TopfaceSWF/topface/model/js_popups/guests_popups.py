from topface.model.model import Model

__author__ = 'ngavrish'

class GuestsPopups(Model):

    def __init__(self,browser,logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def validate_guests_forbidden_nonvip(self):
        print "No validation implemented"
