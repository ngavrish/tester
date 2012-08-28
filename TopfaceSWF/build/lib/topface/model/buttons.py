from topface.model.model import Model

__author__ = 'ngavrish'

class Buttons(Model):

    _top_mark_comment_buttons_id = "btnSendExtra"

    def __init__(self,browser,logger):
        Model.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def send_comment(self,comment_type):
        self.logger.log("Sending comment via button click")
        if comment_type == "topmark":
            self.click(
                self.get_element_by_id(
                    self._top_mark_comment_buttons_id))



