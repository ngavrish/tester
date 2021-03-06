# coding=utf-8
from datetime import datetime
import os
from engine import markup
import time
from dao.dao import DataAccessObject
import settings
import requests


__author__ = 'ngavrish'

class ResultHandler:

    def __init__(self):
        self.build_clean = 1
        self.http_protocol_prefix = "http://" + settings.domain_host + ":" + str(settings.port) + "/"
        self.dao = DataAccessObject()

    def define_failed(self,test_suite):
        for test_case in test_suite:
            if not test_suite[test_case][1]: return True
        return False

    def generate_xml(self,results):
        return []

    def generate_login_data_source_script(self):
        result = "var loginDataChart = ["
        points = self.dao.get_login_graph_data()
        for point in points:
#            parse date
            result += "{\ndate: new Date(\"" + point[1] + "\"),\nseconds: " + str(point[0]) + "\n},"
        result += "];"
        self.save_to_file(result,settings.login_timelog_file)

    def get_stat(self,results):
        failed = 0
        succeed = 0
        for test_suite in results:
            for test_case in results[test_suite]:
                if results[test_suite][test_case][1]:
                    succeed+=1
                else:
                    failed+=1
        return [succeed,failed]


    def generate_html(self,results,build_folder):
        failed = self.get_stat(results)[1]
        succeed = self.get_stat(results)[0]
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
        page.div("Total: " + str(failed+succeed) + " Failed: "  + str(failed) + " Succeed: " + str(succeed),class_="stat_wrapper")
        page.div.close()
        page.table(width="100%")
        for test_suite in results:
            if self.define_failed(results[test_suite]):
                page.tr(class_="failed_tr")
                self.build_clean = 0
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

#    def create_index(self):
#        self.generate_login_data_source_script()
#        page = markup.page()
#        page.init( title="Report Page",
#            encoding='utf-8',
#            charset='utf-8',
#            css=(self.http_protocol_prefix + "includes/reports.css" ),
#            script = {self.http_protocol_prefix + "includes/jquery18.js":'javascript',
#                      self.http_protocol_prefix + "includes/amcharts.js":'javascript'},
#            header="Topface Tests Report",
#            footer="" )
#        page.style(".failed { color: red; }")
#        page.style.close()
#
#        page.scripts({
#            self.http_protocol_prefix + "includes/main_view.js":'javascript',
#            self.http_protocol_prefix + "includes/loginDataChart.js":'javascript',
#            self.http_protocol_prefix + "includes/lineWithLogarithmicAxis.js":'javascript',
#        })
#
#        page.div("<a id='refresh_main_view'>" + u"Обновить" + "</a><a id='start_tests'>" +
#                 u"Запустить тесты" + "</a>", id='management_panel')
#        page.div.close()
#        page.div("<div id='starting_tests_panel'><textarea id='ajax_test_params' name='ajax_test_params'></textarea><br>" +
#                 "<button id='ajax_start_tests'>" + u"Поехали!" + "</button></div>")
#        page.div.close()
#        page.div("<div id=\"chartdiv\" style=\"width: 70%; height: 400px; float:right;\"></div>")
#        page.div.close()
#        self.save_to_file(self.fill_page(page),settings.get_topface_reports_path()+"index.html")
#
#    def fill_page(self,page):
#        builds = self.dao.get_buildhistory()
#        for build in builds:
#            page.p()
#            if build[2]:
#                page.a(build[1],href=build[0])
#            else:
#                page.a(build[1],class_="failed",href=build[0])
#            page.br()
#            page.p.close()
#        return page

    def grab_screenshots_to_current_report_folder(self, folder_name):
        os.chdir(settings.get_topface_reports_path())
        for file in os.listdir("."):
            if file.endswith(".png"):
                os.rename(settings.get_topface_reports_path() + "\\" + file,
                        folder_name + "\\" + file)

    def grab_logs_to_current_report_folder(self, folder_name):
        os.chdir(settings.get_topface_reports_path())
        for file in os.listdir("."):
            if file.endswith(".log"):
                os.rename(settings.get_topface_reports_path() + "\\" + file,
                    folder_name + "\\" + file)

    def handle(self,results):
#        make folder for current report
        new_folder_name = time.strftime("%a_%d_%b_%Y_%H_%M_%S", time.localtime())
        self.current_report_folder = settings.get_topface_reports_path() + new_folder_name
        os.mkdir(self.current_report_folder)
#       handle screenshots
        self.grab_screenshots_to_current_report_folder(self.current_report_folder)
        self.grab_logs_to_current_report_folder(self.current_report_folder)
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
        html_page_name = new_folder_name + "\\" + settings.get_global_topface_reports_name() + ".html"
        stamp = html_page_name[:html_page_name.find("\\")-1].replace("\\","/").split("_")
        name = stamp[1] + " " + stamp[2] + " " + stamp[3] + " " + stamp[4] + ":" + stamp[5] + ":" + stamp[6]
        self.dao.insert_into_buildhistory_table(html_page_name.replace("\\","/"),name,self.build_clean)
        r = requests.post("http://" + settings.domain_host + ":" + settings.port + "/refresh_view")
#        self.create_index()

    def save_to_file(self,file,name):
        result_file = open(name,'w+')
        file_content = str(file).replace("\r\n","<br>")
        result_file.write(file_content)
        result_file.close()