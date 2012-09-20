# coding=utf-8
import os
from engine import markup
import time
import settings


__author__ = 'ngavrish'

class ResultHandler:

#    <?xml version="1.0" encoding="UTF-8"?>
#    <testsuites disabled="" errors="" failures="" name="" tests="" time="">
#    <testsuite disabled="" errors="" failures="" hostname="" id=""
#    name="" package="" skipped="" tests="" time="" timestamp="">
#    <properties>
#    <property name="" value=""/>
#    <property name="" value=""/>
#</properties>
#<testcase assertions="" classname="" name="" status="" time="">
#<skipped/>
#<error message="" type=""/>
#<error message="" type=""/>
#<failure message="" type=""/>
#<failure message="" type=""/>
#<system-out/>
#<system-out/>
#<system-err/>
#<system-err/>
#</testcase>
#<testcase assertions="" classname="" name="" status="" time="">
#<skipped/>
#<error message="" type=""/>
#<error message="" type=""/>
#<failure message="" type=""/>
#<failure message="" type=""/>
#<system-out/>
#<system-out/>
#<system-err/>
#<system-err/>
#</testcase>
#<system-out/>
#<system-err/>
#</testsuite>
#<testsuite disabled="" errors="" failures="" hostname="" id=""
#name="" package="" skipped="" tests="" time="" timestamp="">
#<properties>
#<property name="" value=""/>
#<property name="" value=""/>
#</properties>
#<testcase assertions="" classname="" name="" status="" time="">
#<skipped/>
#<error message="" type=""/>
#<error message="" type=""/>
#<failure message="" type=""/>
#<failure message="" type=""/>
#<system-out/>
#<system-out/>
#<system-err/>
#<system-err/>
#</testcase>
#<testcase assertions="" classname="" name="" status="" time="">
#<skipped/>
#<error message="" type=""/>
#<error message="" type=""/>
#<failure message="" type=""/>
#<failure message="" type=""/>
#<system-out/>
#<system-out/>
#<system-err/>
#<system-err/>
#</testcase>
#<system-out/>
#<system-err/>
#</testsuite>
#</testsuites>
    def __init__(self):
        self.results = []
        self.build_clean = True

    def define_failed(self,test_suite):
        for test_case in test_suite:
            if not test_suite[test_case][1]: return True
        return False

    def generate_xml(self,results):
        return []

    def generate_html(self,results):
        page = markup.page()
        page.init(  title="Report Page",
                    encoding='utf-8',
                    charset='utf-8',
                    css=('..\\includes\\reports.css' ),
                    script = {'..\\includes\\jquery18.js':'javascript'},
                    header="Topface Tests Report",
                    footer="Report End" )
        page.script(src='..\\includes\\index.js')
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
                    page.a(test_case, class_='internal', href= "..\\" + test_case + ".png")
                page.td.close()
                page.tr.close()
        page.table.close()
        return page

    def create_index(self,html_page_name):
        page = markup.page()
        page.init( title="Report Page",
            encoding='utf-8',
            charset='utf-8',
            css=('..\\includes\\reports.css' ),
            script = {'..\\includes\\jquery18.js':'javascript'},
            header="Topface Tests Report",
            footer="" )
        page.style(".failed { color: red; }")
        page.style.close()
        page.p()
        if self.build_clean:
            page.a(html_page_name[:html_page_name.find("\\")-1],href=html_page_name)
        else:
            page.a(html_page_name[:html_page_name.find("\\")-1], class_="failed", href=html_page_name)
        page.p.close()
        self.save_to_file(page,settings.get_topface_reports_path()+"index.html")

    def update_index_report(self,html_page_name):
        os.chdir(settings.get_topface_reports_path())
        for file in os.listdir("."):
            if file == "index.html":
                with open(file, "a") as index_file:
                    if self.build_clean:
                        index_file.write("<p><a href=\"" + html_page_name + "\">" +
                                         html_page_name[:html_page_name.find("\\")-1] + "</a></p>")
                    else:
                        index_file.write("<p><a class=\"failed\" href=\"" + html_page_name + "\">" +
                                         html_page_name[:html_page_name.find("\\")-1] + "</a></p>")
                    index_file.close()
                    return None
        self.create_index(html_page_name)

    def handle(self,results):
#        make folder for current report
        new_folder_name = time.strftime("%a%d%b%Y%H%M%S", time.localtime())
        self.current_report_folder = settings.get_topface_reports_path() + new_folder_name
        os.mkdir(self.current_report_folder)
#        start constructing reports
        self.results = results
        html_page = self.generate_html(results)
        html_page_name = self.current_report_folder + "\\" +\
                         settings.get_global_topface_reports_name() + ".html"
        xml_page = self.generate_xml(results)
        xml_page_name = self.current_report_folder +\
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