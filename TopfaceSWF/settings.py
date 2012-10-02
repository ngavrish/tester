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

#  Fixed topface global reports name
__global_reports_name = "TopfaceSFW"

test_packages = ["model_tests","research_tests"]

#   test suite to run
testsuite = ["messages_test"]#,
# List of all possible test plans = "login_test", "marks_test", "messages_test", "profile_test"]

#   selenium server host
server_host = "http://localhost:4444"

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

#   reporting-server host
report_host = '192.168.2.87'
local_host = 'localhost'

#   reporting-server port
report_port = 8888

#port/host that are finally setup in srv.py from cmd-parsing to start paste
paste_host = ""
paste_port = ""

#topface database name
topface_db = 'topface.db'

#login timeline log
login_timelog_file = __reports_path +  "\\includes\\loginDataChart.js"

def get_product_name():
    return __product_name

def get_topface_reports_path():
    return __reports_path

def get_global_topface_reports_name():
    return __global_reports_name