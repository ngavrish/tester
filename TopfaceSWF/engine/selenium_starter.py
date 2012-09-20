import inspect
import sys
from reports.result_handler import ResultHandler
import settings
import topface

__author__ = 'ngavrish'

class SeleniumStarter:

    def __init__(self):
        self.test_suite = []
        self.test_package= settings.get_product_name()
        self.browser_mapping = {}
        self.global_log = {}

    def get_testsuite_instances(self):
        __import__(settings.get_product_name()+".browser_mapping")
        modules = inspect.getmembers(sys.modules[settings.get_product_name()])
        for module in modules:
            if str(module[1]).find("module") > -1 and module[0].endswith("browser_mapping"):
                self.browser_mapping = module[1].browser_mapping

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
                            instance = class_tuple[1]()
                            try:
                                print test_suite_name + ": " + self.browser_mapping.get(test_suite_name)
                                instance.set_browser_name(self.browser_mapping.get(test_suite_name))
                                self.test_suite.append(instance)
                            except TypeError as e:
                                print "Browser not found for " + test_suite_name + ": " + e.message
                                raise
                except ImportError as e:
                    print test_suite_module_name + " not found in project path: " + e.message

    def start_consequent(self):
        self.get_testsuite_instances()
        for test in self.test_suite:
            test_suite_result = test.run()
            {}.keys()
            for item in test_suite_result:
                print item + " has " + str(len(test_suite_result[item])) + " test cases"
            self.global_log[test_suite_result.keys()[0]] = test_suite_result.values()[0]

        print "Result  = \n\r" + str(self.global_log) + "\n\r ======================= "
        result_handler = ResultHandler()
        result_handler.handle(self.global_log)

    def generate_parallel_start_command(self):
        pass

    def start_parallel(self):
        pass
