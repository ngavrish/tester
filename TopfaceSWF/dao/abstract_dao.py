from abc import ABCMeta
import sqlite3 as lite
import settings

__author__ = 'ngavrish'

class AbstractDataAccessObject:

    __metaclass__ = ABCMeta

    def __init__(self):
        self.con = lite.connect(settings.topface_db)
        self.cursor = self.con.cursor()

    def drop_table(self,table_name):
        pass

    def execute_statement(self,statement,*params):
        pass