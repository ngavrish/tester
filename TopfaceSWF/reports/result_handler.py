# coding=utf-8
from engine import markup
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

    def define_failed(self,test_suite):
        for name in test_suite:
            for test_case in test_suite[name]:
                if not test_case[1]:
                    return True
        return False

    def generate_xml(self,results):
        for test_suite in results:
            for name in test_suite:
                for test_case in test_suite[name]:
                    if not test_suite[name][test_case][1]:
                        print "Test Failed"
                    else:
                        print "Test Passed"
                    return test_suite[name][test_case][0]
                #                    print test_case + ": " + str(test_suite[name][test_case])

    def generate_html(self,results):
        page = markup.page()
        page.init( title="My title",
                    encoding='utf-8',
                    charset='utf-8',
                    css=(settings.get_topface_reports_path() + 'includes\\reports.css' ),
                    script = {settings.get_topface_reports_path() + "includes\\jquery18.js":'javascript'},
                    header="Something at the top",
                    footer="The bitter end." )
        page.script(src=settings.get_topface_reports_path() + "includes\\index.js")
        page.script.close()
        page.table(width="100%")
        for test_suite in results:
            for name in test_suite:
                if self.define_failed(test_suite):
                    page.tr(class_="failed_tr")
                else:
                    page.tr(class_="passed_tr")
                page.td()
                page.p(name)
                page.td.close()
                page.tr.close()
                #                print name + " is: " + str(test_suite[name])
                for test_case in test_suite[name]:
                    page.tr()
                    page.td(width="50%")
                    page.a(test_case, class_='test_case', id=test_case, href='#')
                    page.br()
                    page.div(class_ = "log_content",id=test_case+"_content")
                    page.span(test_suite[name][test_case][0])
                    page.div.close()
                    page.td.close()
                    page.td(width="50%")
                    if not test_suite[name][test_case][1]:
                        page.a(test_case, class_='internal', href=test_case + ".png")
                    page.td.close()
                    page.tr.close()
#                    print test_case + ": " + str(test_suite[name][test_case])
        page.table.close()
        return page

    def handle(self,results):
        self.results = results
        self.save_to_file(
            self.generate_html(results),settings.get_topface_reports_path() +
                                        settings.get_global_topface_reports_name() + ".html")
        self.save_to_file(
            self.generate_xml(results),settings.get_topface_reports_path() +
                                       settings.get_global_topface_reports_name() + ".xml")

    def save_to_file(self,file,name):
        result_file = open(name,'w+')
        file_content = str(file).replace("\r\n","<br>")
        result_file.write(file_content)
        result_file.close()