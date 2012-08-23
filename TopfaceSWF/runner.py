import getopt
import inspect
import re
import sys
from engine.selenium_starter import SeleniumStarter
import settings

__author__ = 'user'


def main(argv=None):
    if argv is None:
        argv = sys.argv
    for option in argv[1:]:
        if option.find("-p") > -1:
            settings.parallel = True
        if option.find("-s") > -1:
            settings.slow_mode = True
        if option.find("testsuite") > -1:
            settings.testsuite = re.split('\W+',option.split("=")[1])
        if option.find("server_host") > -1:
            settings.server_host = option.split("=")[1]
        if option.find("remote_port") > -1:
            settings.remote_port = option.split("=")[1]
        if option.find("target_url") > -1:
            settings.target_url = option.split("=")[1]
        if option.find("remoute_amount") > -1:
            settings.remote_amount = option.split("=")[1]

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    starter = SeleniumStarter()

    starter.start_consequent()
#    sys.exit(main())