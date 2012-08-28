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

#   To run selenium framework you need to have
#   Selenium jar-files and specific drivers somewhere on your File System
__selenium_path = "C:\\selenium"


#   test suite to run
testsuite = ["marks_test"]

#   selenium server host
server_host = "http://localhost:4444"

#   target testing url
target_url = "http://topface.com"

#   remote web driver port number
remote_port = 5555

#   Amount of remote instances running at once
remote_amount = 1

#   Specifies if tests
parallel = False

#   Specifies it tests run in slow mode
slow_mode = False

#   Wait for element time in seconds
wait_for_element_time = 10

def get_product_name():
    return __product_name

def get_topface_reports_path():
    return __reports_path

