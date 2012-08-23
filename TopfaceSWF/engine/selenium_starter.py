import inspect
import sys
import settings

__author__ = 'user'

class SeleniumStarter:

    def __init__(self):
        self.test_suite = []
        self.test_package = settings.get_product_name() + ".model_tests."
        self.browser_mapping = {}

    def get_testsuite_instances(self):
        __import__(settings.get_product_name()+".browser_mapping")
        modules = inspect.getmembers(sys.modules[settings.get_product_name()])
        for module in modules:
            if str(module[1]).find("module") > -1 and module[0].endswith("browser_mapping"):
                self.browser_mapping = module[1].browser_mapping

        for test_suite_name in settings.testsuite:
#            for name, obj in inspect.getmembers(sys.modules[]):
            test_suite_module_name = self.test_package + test_suite_name
            __import__(test_suite_module_name)
            classes = inspect.getmembers(sys.modules[test_suite_module_name], inspect.isclass)
            for class_tuple in classes:
                if class_tuple[0].endswith("TestSuite") and class_tuple[0] != "TestSuite":
                    print class_tuple[0] + ": " + str(class_tuple[1])
                    instance = class_tuple[1]()

                    print test_suite_name + ": " + self.browser_mapping.get(test_suite_name)
                    instance.set_browser_name(self.browser_mapping.get(test_suite_name))
                    self.test_suite.append(instance)




    def start_consequent(self):
        self.get_testsuite_instances()
        for test in self.test_suite:
            test.run()

    def generate_parallel_start_command(self):
        pass

    def start_parallel(self):
        pass
