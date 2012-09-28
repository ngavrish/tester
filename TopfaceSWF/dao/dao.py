import sqlite3 as lite
import sys
from abstract_dao import AbstractDataAccessObject
import settings

__author__ = 'ngavrish'

class DataAccessObject(AbstractDataAccessObject):

    def __init__(self):
        super(DataAccessObject, self).__init__()

    def create_login_timline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS LOGIN_TIMELINE(Id INT, seconds REAL)")

    def insert_into_login_timeline_table(self):
        pass

    def delete_from_login_timeline_table(self):
        pass

    def create_mark_user_timeline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS MARK_USER_TIMELINE(Id INT, seconds REAL)")

    def insert_into_mark_user_timeline_table(self):
        pass

    def delete_from_mark_user_timeline_table(self):
        pass

    def create_send_message_timeline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS SEND_MESSAGE_TIMELINE(Id INT, seconds REAL)")

    def insert_into_send_message_timeline_table(self):
        pass

    def delete_from_send_message_timeline_table(self):
        pass

    def create_user_navigation_timeline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS NAVIGATION_TIMELINE(Id INT, seconds REAL)")

    def insert_into_user_navigation_timeline_table(self):
        pass

    def delete_from_user_navigation_timeline_table(self):
        pass

    def create_questionary_editing_timeline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS QUESTIONATY_EDITING_TIMELINE(Id INT, seconds REAL)")

    def insert_into_questionary_timeline_table(self):
        pass

    def delete_from_questionary_timeline_table(self):
        pass