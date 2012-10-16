# coding=utf-8
from engine.test_failed_exception import TestFailedException
from topface.model.xml_model import XMLModel

__author__ = 'ngavrish'

class XMLTestExecutor(XMLModel):
    """
        Class for parsing parameters and executing commands below:
        <commands>

        <!--simple actions-->
        <click xpath="div[@id='id']" />
        <enterText xpath="div[@id='']" text="text"/>
        <selectFromDropdownByIndex dropdownXpath="xpath" elementIndex="index" />
        <selectFromDropdownByValue dropdownXpath="xpath" elementValue="value" />
        <selectFromDropdownByText  dropdownXpath="xpath" elementText="text" />
        <hover xpath="xpath" />

        <!--business actions-->
        <authorize user="User1" platform="fb-sa" />
        <markUser markValue="5" markAmount="1" />
        <filterCity cityName="Киев" />

        <!--window actions-->
        <openUrl url="url" />
        <switchToPopup/>
        <switchToRoot/>
        <logout/>
        <close/>

        <assertText xpath="xpath" expectedText="expValue"/>
        <assertAttribute xpath="xpath" expectedValue="attribute" />
        <assertHtml xpath="xpath" expectedHtml="Html"/>
        <assertElemen xpath="xpath" />

        </commands>
    """

    def __init__(self, browser, logger):
        super(XMLTestExecutor, self).__init__(browser, logger)
        self.browser = browser
        self.logger = logger
        self.commands = {
            "click": self.click,
            "enter_text": self.enter_text,
            "select_from_dropdown_by_index": self.select_from_dropdown_by_index,
            "select_from_dropdown_by_value": self.select_from_dropdown_by_value,
            "select_from_dropdown_by_text": self.select_from_dropdown_by_text,
            "hover": self.hover,
            "authorize": self.authorize,
            "mark_user": self.mark_user,
            "filter_city": self.filter_city,
            "open_url": self.open_url,
            "switch_to_popup": self.switch_to_popup,
            "switch_to_root": self.switch_to_root,
            "logout": self.logout,
            "close": self.close,
            "assert_text": self.assert_text,
            "assert_attribute": self.assert_attribute,
            "assert_html": self.assert_html,
            "assert_element": self.assert_element
        }
        self.parameters_list = ["value", "amount", "platform", "xpath", "time_delta", "coords"]

    def execute_command(self,command,parameters):
        method_params = {}
        for param_item in self.parameters_list:
            if param_item in parameters.keys():
                method_params[param_item] = parameters[param_item]
            else:
                method_params[param_item] = None
        try:
            print "next command = " + command
            self.commands[command](xpath=method_params["xpath"],
                                    value=method_params["value"],
                                    amount=method_params["amount"],
                                    time_delta=method_params["time_delta"],
                                    platform=method_params["platform"],
                                    coords=method_params["coords"])
        except Exception as e:
            raise TestFailedException("Failed to execute command = " + command + " with parameters = " + str(method_params))