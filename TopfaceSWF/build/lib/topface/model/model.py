from selenium.webdriver.support.wait import WebDriverWait

__author__ = 'ngavrish'


class Model:

    def __init__(self,browser,logger):
        self.browser = browser
        self.logger = logger

    def get_element_xpath(self, element):
        self.logger.log("Getting element = " + str(element) + "xpath ")
        return self.browser.\
                execute_script(
                                "gPt=function(c){if(c.id!==''){return'id(\"'+c.id+'\")'}if(c===document.body){return c.tagName}var a=0;var e=c.parentNode.childNodes;for(var b=0;b<e.length;b++){var d=e[b];if(d===c){return gPt(c.parentNode)+'/'+c.tagName+'['+(a+1)+']'}if(d.nodeType===1&&d.tagName===c.tagName){a++}}};return gPt(arguments[0]).toLowerCase();",element)

    def click(self, element):
        self.logger.log("Click Element = " + self.get_element_xpath(element))
        element.click()

    def get_element_by_xpath(self,xpath):
        self.logger.log("Find element by XPATH = " + xpath)
        return self.browser.find_element_by_xpath(xpath)

    def get_element_by_id(self,id):
        self.logger.log("Find element by ID = " + id)
        return self.browser.find_element_by_id(id)

    def hover(self):
        pass

    def drag_and_drop(self):
        pass

    def click_and_hold(self):
        pass

    def key_down(self):
        pass

    def switch_to_popup(self):
        pass

    def switch_from_popup(self):
        pass

    def enter_text(self):
        pass

    def wait4xpath(self,time,xpath):
        self.logger.log("Waiting for element XPATH = " + xpath)
        return WebDriverWait(self.browser, time).until(lambda driver: driver.find_element_by_xpath(xpath))

    def wait4id(self,time,id):
        self.logger.log("Waiting for element ID = " + id)
        return WebDriverWait(self.browser, time).until(lambda driver: driver.find_element_by_id(id))