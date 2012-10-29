import httplib
import json
import re
from paste.request import parse_formvars
from dao.dao import DataAccessObject
from engine.selenium_starter import SeleniumStarter
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
        self.root_app['/update'] = self.refresh_view
        self.root_app['/start'] = self.start_tests

    def parse_settings(self,args):
        try:
            if args is not None:
                if isinstance(args, basestring):
                    args = args.split(' ')
                print "ARGS = " + str(args)
                for option in args:
                    if option.find("-p") > -1:
                        settings.parallel = True
                    if option.find("-s") > -1:
                        settings.slow_mode = True
                    if option.find("testsuite") > -1:
                        settings.testsuite = re.split('\W+',option.split("=")[1])
                    if option.find("xml_testsuite") > -1:
                        settings.xml_testsuite = re.split('\W+',option.split("=")[1])
                    if option.find("remote_port") > -1:
                        settings.remote_port = option.split("=")[1]
                    if option.find("target_url") > -1:
                        settings.target_url = option.split("=")[1]
                    if option.find("browser") > -1:
                        settings.global_browser = option.split("=")[1]
                    if option.find("remoute_amount") > -1:
                        settings.remote_amount = option.split("=")[1]
        except Exception as e:
            raise

    def start_tests(self,environ,start_response):
        param_string = parse_formvars(environ)['params']
        try:
            self.parse_settings(param_string)
            SeleniumStarter().start()
            start_response('200 Ok', [('content-type', 'text/html')])
            return ["OK"]
        except Exception as e:
            start_response('200 Ok', [('content-type', 'text/html')])
            return ["ERROR"]

    def refresh_view(self,environ,start_response):
        ResultHandler().generate_login_data_source_script()
        dao = DataAccessObject()
        builds = dao.get_buildhistory()
        start_response('200 Ok', [('content-type', 'application/json')])
        return [json.dumps(builds)]

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