import httplib
from paste import fileapp, httpserver
import settings

class ReportServer:

    def __init__(self):
        pass

    def if_server_is_running(self):
        hh = None
        connectionType = httplib.HTTPConnection
        try:
            hh = connectionType(settings.report_host, settings.report_port)
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

    def start_server(self):
        try:
            app = fileapp.DirectoryApp(settings.get_topface_reports_path())
            httpserver.serve(app, settings.report_host, settings.report_port)
        except Exception:
            print "Couldn't start server"
            raise

if __name__ == "__main__":
    ReportServer().start_server()