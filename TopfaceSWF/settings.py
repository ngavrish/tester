import os

__author__ = 'ngavrish'

#    Initialized on tests start from command line arguments
#    Contains framework settings that manage tests running
#    -p -------------- when used means 'run tests in parallel'
#    -s -------------- option when used means 'run tests in slow mode'
#    testsuite ------- comma separated names of test plans to run
#    server_host ----- server for Selenium hub or stand-alone server
#    remote_port ----- port number for selenium remote web driver
#    remote_amount --- amount of remote instances running at once

#   Test Suite to Web Browser mapper.
#   This dictionary stores information on what testsuite should run under which browser
#
#   "login_test":"firefox" - this entry means that login_test suite will run under firefox

#    product name
__product_name = "topface"

#   root path for test reports
__reports_path = os.path.dirname(os.path.abspath(__file__)) + "\\topface_reports\\"

#   root path for xml test cases
__xml_test_cases_path = os.path.dirname(os.path.abspath(__file__)) + "\\xml_test_cases\\"

#   To run selenium framework you need to have
#   Selenium jar-files and specific drivers somewhere on your File System
__selenium_path = "C:\\selenium"

#  Fixed topface global reports name
__global_reports_name = "TopfaceSFW"

test_packages = ["model_tests","research_tests"]

#   if global browser is set, no browser mapping used
global_browser = None

#   test suite to run
testsuite = ["login_test", "marks_test", "messages_test", "profile_test"]#,

#   xml test suites to run
xml_testsuite = ["demo_xml"]

# List of all possible test plans = "login_test", "marks_test", "messages_test", "profile_test"]

# demo_xml
#   target testing url
prod = "http://topface.com"
delta = "http://delta.topface.com"
alpha = "http://alpha.topface.com"
target_url = prod

#   remote web driver port number
remote_port = 5555

#   Amount of remote instances running at once
remote_amount = 1

#   Specifies if tests
parallel = False

#   Specifies it tests run in slow mode
slow_mode = False

#   Wait for element time in seconds. Max value = 10. > 10 -> fails
wait_for_element_time = 10

#   amount of likes for research
like_amount = 2

#   amount of marks for research
mark_amount = 100

#   reporting-server host/port
domain_host = "tester84"
host = '0.0.0.0'
port = "8888"

#topface database name
topface_db = 'topface.db'

#login timeline log
login_timelog_file = __reports_path +  "\\includes\\loginDataChart.js"

def get_product_name():
    return __product_name

def get_topface_reports_path():
    return __reports_path

def get_xml_testsuites_path():
    return __xml_test_cases_path

def get_global_topface_reports_name():
    return __global_reports_name