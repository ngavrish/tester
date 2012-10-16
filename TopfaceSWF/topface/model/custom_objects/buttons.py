from topface.model.object_model import ObjectModel

__author__ = 'ngavrish'

class Buttons(ObjectModel):

    _top_mark_comment_buttons_id = "btnSendExtra"

    def __init__(self,browser,logger):
        ObjectModel.__init__(self, browser, logger)
        self.browser = browser
        self.logger = logger

    def send_comment(self,comment_type):
        self.logger.log("Sending comment via button click")
        if comment_type == "topmark":
            self.click(
                self.get_element_by_id(
                    self._top_mark_comment_buttons_id))



