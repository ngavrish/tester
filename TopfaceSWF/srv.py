import httplib
import re
from paste import fileapp, httpserver
import sys
from paste.urlmap import URLMap
from reports.result_handler import ResultHandler
import settings

def main():
    #if argv is None:
    #    argv = sys.argv
#        check if we have something passed to the arguments
    #settings.paste_host = settings.local_host
    #settings.paste_port = settings.paste_port
    #for option in argv[1:]:
    #    if option.find("host") > -1:
    #        settings.paste_host = option.split("=")[1]
    #    if option.find("port") > -1:
    #        settings.paste_port = option.split("=")[1]
    ReportServer().start_server(settings.host,settings.port)
#        setup default values from settings.py

class ReportServer:

    def __init__(self):
        self.root_app = URLMap()
        self.root_app['/'] = fileapp.DirectoryApp(settings.get_topface_reports_path())
        self.root_app['/update'] = self.update_view


    def update_view(self, environ, start_response):
        result_handler = ResultHandler()
        result_handler.create_index()
        start_response('200 Ok', [('content-type', 'text/html')])
        return ["OK"]

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

    def start_server(self, host=settings.host, port=settings.port):
        try:
            print "starting at " + host + ":" + port
            httpserver.serve(self.root_app, host, int(port))
        except Exception:
            print "Couldn't start server"
            raise

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding("utf-8")
    main()