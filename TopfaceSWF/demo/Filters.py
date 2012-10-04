__author__ = 'ngavrish'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re

class Filtrs(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://topface.com/"
        self.verificationErrors = []

    def test_filtrs(self):
        driver = self.driver
        driver.find_element_by_xpath(u"//a[text()='мужчины']").click()
        # ERROR: Caught exception [ERROR: Unsupported command [mouseMoveAt]]
        driver.find_element_by_xpath("//div[contains(@class,'dropdown-head')]/a[contains(@class,'age-filter')]").click()
        # ERROR: Caught exception [ERROR: Unsupported command [dragAndDrop]]
        # ERROR: Caught exception [ERROR: Unsupported command [mouseMoveAt]]
        driver.find_element_by_xpath("//div[contains(@class,'close')]").click()
        # ERROR: Caught exception [ERROR: Unsupported command [mouseMoveAt]]
        driver.find_element_by_xpath("//a[contains(@class,'city-filter')]").click()
        driver.find_element_by_xpath("//input[@id='datingCityAc']").click()
        driver.find_element_by_xpath("//input[@id='datingCityAc']").send_keys(u"Москва, Россия")
        # ERROR: Caught exception [ERROR: Unsupported command [mouseMoveAt]]
        driver.find_element_by_xpath("//a[@id='ui-active-menuitem']").click()
        # ERROR: Caught exception [ERROR: Unsupported command [mouseMove]]
        driver.find_element_by_xpath("//a[contains(@class,'univer-filter')]").click()
        driver.find_element_by_xpath("//input[@id='datingUniverAc']").click()
        driver.find_element_by_xpath("//input[@id='datingUniverAc']").send_keys(u"МГУ")
        # ERROR: Caught exception [ERROR: Unsupported command [mouseMoveAt]]
        driver.find_element_by_xpath("//a[@id='ui-active-menuitem']").click()
        for i in range(60):
            try:
                if self.is_element_present(By.XPATH, "//div[contains(@class,'user-icons')]//div[@id='onlineStatus' and contains(@style,'display: block;')]/../div[3]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

