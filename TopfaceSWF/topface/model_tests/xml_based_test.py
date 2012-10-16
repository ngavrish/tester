from engine.test_suite import TestSuite
from engine.test_case import TestCase
from xml.dom.minidom import *
import settings
from engine.xml_test_executor import XMLTestExecutor

__author__ = 'ngavrish'

class XMLTestSuite(TestSuite):

    def __init__(self,name):
        TestSuite.__init__(self,name)
        self.test_cases = []
        self.result = {}

    def run(self,xml_source):
        test_suite = parse(settings.get_xml_testsuites_path() + xml_source)
        test_cases = test_suite.getElementsByTagName('testcase')
        for test_case in test_cases:
            self.test_cases.append(self.XMLTestCase(test_case.getAttribute("name"),test_case.childNodes))
        for test_case in self.test_cases:
            run_test_results = test_case.run_test()
            self.result[run_test_results.keys()[0]] = run_test_results.values()[0]
        return {xml_source[:xml_source.rfind(".xml")]: self.result}

    class XMLTestCase(TestCase):

        def __init__(self,test_name,test_case_xml):
            self.set_log_name(test_name)
            self.source = test_case_xml

        def run(self, browser, logger):
            print "SOURCE = " + str(self.source)
            for step in self.source:
                self.logger.log("STEP = " + str(step))
                if step.nodeType == Node.ELEMENT_NODE:
                    params = {}
                    if step.tagName == "browser":
                        XMLTestSuite.browser_name = step.getAttribute(step.tagName)
                    else:
                        for attr_i in range(len(step.attributes)):
                            params[step.attributes.item(attr_i).name] = step.attributes.item(attr_i).value
                        XMLTestExecutor(browser,logger).execute_command(command=step.tagName,parameters=params)
