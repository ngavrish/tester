import httplib
import re
from paste import fileapp, httpserver
import sys
import settings

def main(argv=None):
    if argv is None:
        argv = sys.argv
#        check if we have something passed to the arguments
    settings.paste_host = settings.local_host
    settings.paste_port = settings.paste_port
    for option in argv[1:]:
        if option.find("host") > -1:
            settings.paste_host = option.split("=")[1]
        if option.find("port") > -1:
            settings.paste_port = option.split("=")[1]

#        setup default values from settings.py

class ReportServer:

    def __init__(self):
        pass

    def server_is_running(self,host,port):
        connectionType = httplib.HTTPConnection
        try:
            hh = connectionType(host, port)
            hh.request('GET', '/index.html')
            resp = hh.getresponse()
            headers = resp.getheaders()
            if headers:
                if ('server', 'PasteWSGIServer/0.5 Python/2.7.3') in headers:
                    return True
            else:
                return False
        except Exception:
            return False

    def start_server(self, paste_host=settings.ip_host, paste_port=settings.paste_port):
        try:
            app = fileapp.DirectoryApp(settings.get_topface_reports_path())
            print "starting at " + paste_host + ":" + paste_port
            httpserver.serve(app, paste_host, int(paste_port))
        except Exception:
            print "Couldn't start server"
            raise

if __name__ == "__main__":
    main()
    ReportServer().start_server(settings.paste_host,settings.paste_port)