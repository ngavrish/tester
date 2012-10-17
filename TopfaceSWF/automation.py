import re
import subprocess
import sys
from engine.selenium_starter import SeleniumStarter
import settings
from srv import ReportServer

__author__ = 'ngavrish'

def main(args=None):
    ReportServer().parse_settings(args)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    main()
    report_server = ReportServer()
    if not report_server.server_is_running(settings.host,settings.port):
        subprocess.Popen("python srv.py " + "host=" + settings.host + " port=" + str(settings.port))
    SeleniumStarter().start()

#    sys.exit(main())