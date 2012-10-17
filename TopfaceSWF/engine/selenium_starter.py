import inspect
import os
import sys
from reports.result_handler import ResultHandler
from dao.dao import DataAccessObject
import settings
import topface
from topface.model_tests.xml_based_test import XMLTestSuite

__author__ = 'ngavrish'

class SeleniumStarter:

    def __init__(self):
        self.test_suites = []
        self.xml_testsuite_files = []
        self.test_package= settings.get_product_name()
        self.browser_mapping = {}
        self.global_log = {}

    def start(self):
        self.setup_database()
        if not settings.parallel:
            self.start_consequent()
        else:
            self.start_parallel()

    def setup_database(self):
        dao = DataAccessObject()
        dao.create_login_timline_table()
        dao.create_mark_user_timeline_table()
        dao.create_user_navigation_timeline_table()
        dao.create_questionary_editing_timeline_table()
        dao.create_send_message_timeline_table()
        dao.create_buildhistory_table()


    def get_testsuite_instances(self):
        for test_suite_name in settings.testsuite:
#            for name, obj in inspect.getmembers(sys.modules[]):
            for test_package_name in settings.test_packages:
                test_suite_module_name = self.test_package + "." + test_package_name + "." + test_suite_name
                print "Module name = " + test_suite_module_name
                try:
                    __import__(test_suite_module_name)
                    classes = inspect.getmembers(sys.modules[test_suite_module_name], inspect.isclass)
                    for class_tuple in classes:
                        if class_tuple[0].endswith("TestSuite") and class_tuple[0] != "TestSuite":
                            print class_tuple[0] + ": " + str(class_tuple[1])
                            instance = class_tuple[1](test_suite_name)
                            self.test_suites.append(instance)
                except ImportError as e:
                    print test_suite_module_name + " not found in project path: " + e.message

    def start_pure_python_testsuites(self):
        self.get_testsuite_instances()
        for test in self.test_suites:
            test_suite_result = test.run()
            for item in test_suite_result:
                print item + " has " + str(len(test_suite_result[item])) + " test cases"
            self.global_log[test_suite_result.keys()[0]] = test_suite_result.values()[0]

    def get_xml_testsuites(self):
        dirList=os.listdir(settings.get_xml_testsuites_path())
        for fname in dirList:
            if fname.endswith(".xml") and fname[:fname.rfind(".xml")] in settings.xml_testsuite:
                self.xml_testsuite_files.append(fname)
                print "XML FILENAME = " + fname

    def start_xml_testsuites(self):
        self.get_xml_testsuites()
        for test in self.xml_testsuite_files:
            test_suite_result = XMLTestSuite(test[:test.rfind(".xml")]).run(test)
            for item in test_suite_result:
                print item + " has " + str(len(test_suite_result[item])) + " test cases"
            self.global_log[test_suite_result.keys()[0]] = test_suite_result.values()[0]

    def start_consequent(self):
        __import__(settings.get_product_name()+".browser_mapping")
        modules = inspect.getmembers(sys.modules[settings.get_product_name()])
        for module in modules:
            if str(module[1]).find("module") > -1 and module[0].endswith("browser_mapping"):
                self.browser_mapping = module[1].browser_mapping

        self.start_pure_python_testsuites()
        self.start_xml_testsuites()
        print "Result  = \n\r" + str(self.global_log) + "\n\r ======================= "
        result_handler = ResultHandler()
        result_handler.handle(self.global_log)

    def generate_parallel_start_command(self):
        pass

    def start_parallel(self):
        pass
