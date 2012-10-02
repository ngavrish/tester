# coding=utf-8
from datetime import datetime
import os
from engine import markup
import time
from dao.dao import DataAccessObject
import settings


__author__ = 'ngavrish'

class ResultHandler:

    def __init__(self):
        self.build_clean = True
        self.http_protocol_prefix = "http://" + settings.report_host + ":" + str(settings.report_port) + "/"

    def define_failed(self,test_suite):
        for test_case in test_suite:
            if not test_suite[test_case][1]: return True
        return False

    def generate_xml(self,results):
        return []

    def generate_login_data_source_script(self):
        dao = DataAccessObject()
        result = "var loginDataChart = ["
        points = dao.get_login_graph_data()
        for point in points:
#            parse date
            result += "{\ndate: new Date(\"" + point[1] + "\"),\nseconds: " + str(point[0]) + "\n},"
        result += "];"
        self.save_to_file(result,settings.login_timelog_file)

    def generate_html(self,results,build_folder):
        page = markup.page()
        page.init(  title="Report Page",
                    encoding='utf-8',
                    charset='utf-8',
                    css=(self.http_protocol_prefix + "includes/reports.css" ),
                    script = {self.http_protocol_prefix + "includes/jquery18.js":'javascript'},
                    header="Topface Tests Report",
                    footer="Report End" )
        page.script(src=self.http_protocol_prefix + "includes/index.js")
        page.script.close()
        page.table(width="100%")
        for test_suite in results:
            if self.define_failed(results[test_suite]):
                page.tr(class_="failed_tr")
                self.build_clean = False
            else:
                page.tr(class_="passed_tr")
            page.td()
            page.p(test_suite)
            page.td.close()
            page.tr.close()

            for test_case in results[test_suite]:
                page.tr()
                page.td(width="50%")
                if results[test_suite][test_case][1]:
                    page.a(test_case, class_='test_case', id=test_case, href='#')
                else:
                    page.a(test_case, class_='test_case failed', id=test_case, href='#')
                page.br()
                page.div(class_ = "log_content",id=test_case+"_content")
                page.span(results[test_suite][test_case][0])
                page.div.close()
                page.td.close()
                page.td(width="50%")
                if not results[test_suite][test_case][1]:
                    page.a(test_case, class_='internal', href= self.http_protocol_prefix + build_folder + "/"
                                                               + test_case + ".png")
                page.td.close()
                page.tr.close()
        page.table.close()
        return page

    def create_index(self,html_page_name):
        build_folder = html_page_name[:html_page_name.find("\\")-1].replace("\\","/")
        page = markup.page()
        page.init( title="Report Page",
            encoding='utf-8',
            charset='utf-8',
            css=(self.http_protocol_prefix + "includes/reports.css" ),
            script = {self.http_protocol_prefix + "includes/jquery18.js":'javascript'},
            header="Topface Tests Report",
            footer="" )
        page.style(".failed { color: red; }")
        page.style.close()

        page.scripts({
           self.http_protocol_prefix + "includes/loginDataChart.js":'javascript',
           self.http_protocol_prefix + "includes/lineWithLogarithmicAxis.js":'javascript',
           self.http_protocol_prefix + "includes/amcharts.js":'javascript'
        })

        page.scripts.close()
        page.div("<div id=\"chartdiv\" style=\"width: 70%; height: 400px; float:right;\"></div>")
        page.div.close()

        page.p()
        if self.build_clean:
            page.a(build_folder,href=html_page_name.replace("\\","/"))
        else:
            page.a(build_folder, class_="failed", href=html_page_name.replace("\\","/"))
        page.p.close()
        self.save_to_file(page,settings.get_topface_reports_path()+"index.html")

    def update_index_report(self,html_page_name):
        build_folder = html_page_name[:html_page_name.find("\\")-1].replace("\\","/")
        os.chdir(settings.get_topface_reports_path())
        for file in os.listdir("."):
            if file == "index.html":
                with open(file, "a") as index_file:
                    if self.build_clean:
                        index_file.write("<p><a href=\"" + html_page_name.replace("\\","/") + "\">" +
                                         build_folder + "</a></p>")
                    else:
                        index_file.write("<p><a class=\"failed\" href=\"" + html_page_name.replace("\\","/") + "\">" +
                                         build_folder + "</a></p>")
                    index_file.close()
                    return None
        self.create_index(html_page_name)

    def grab_screenshots_to_current_report_folder(self, folder_name):
        os.chdir(settings.get_topface_reports_path())
        for file in os.listdir("."):
            if file.endswith(".png"):
                os.rename(settings.get_topface_reports_path() + "\\" + file,
                        folder_name + "\\" + file)

    def handle(self,results):
        self.generate_login_data_source_script()
#        make folder for current report
        new_folder_name = time.strftime("%a%d%b%Y%H%M%S", time.localtime())
        self.current_report_folder = settings.get_topface_reports_path() + new_folder_name
        os.mkdir(self.current_report_folder)
#       handle screenshots
        self.grab_screenshots_to_current_report_folder(self.current_report_folder)
#       start constructing reports
        html_page = self.generate_html(results,new_folder_name)
        html_page_name = self.current_report_folder + "\\" +\
                         settings.get_global_topface_reports_name() + ".html"
        xml_page = self.generate_xml(results)
        xml_page_name = self.current_report_folder + "\\" +\
                        settings.get_global_topface_reports_name() + ".xml"
        self.save_to_file(
            html_page,html_page_name)
        self.save_to_file(
            xml_page,xml_page_name)
#        prepare index-reporting file
        self.update_index_report(new_folder_name + "\\" + settings.get_global_topface_reports_name() + ".html")

    def save_to_file(self,file,name):
        result_file = open(name,'w+')
        file_content = str(file).replace("\r\n","<br>")
        result_file.write(file_content)
        result_file.close()