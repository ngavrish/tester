from datetime import datetime
import sqlite3 as lite
import sys
from abstract_dao import AbstractDataAccessObject
import settings

__author__ = 'ngavrish'

class DataAccessObject(AbstractDataAccessObject):

    def __init__(self):
        super(DataAccessObject, self).__init__()

    def create_login_timline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS LOGIN_TIMELINE(Id INTEGER PRIMARY KEY AUTOINCREMENT, seconds REAL, event_time TEXT)")

    def insert_into_login_timeline_table(self,delta):
        try:
            self.cursor.execute("INSERT INTO LOGIN_TIMELINE('seconds','event_time') VALUES (?,?)",
                                (str("%0.2f" % delta),datetime.now().strftime("%m/%d/%Y %H:%M")))
        except Exception as e:
            print e
            raise
        print "INSERTED"
        self.con.commit()
        print "COMMITED"
        self.con.close()
        print "CLOSED"

    def delete_from_login_timeline_table(self):
        self.con.close()

    def get_login_graph_data(self):
        self.cursor.execute("SELECT SECONDS, EVENT_TIME from LOGIN_TIMELINE")
        return self.cursor.fetchall()

    def create_mark_user_timeline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS MARK_USER_TIMELINE(Id INTEGER PRIMARY KEY AUTOINCREMENT, seconds REAL)")

    def insert_into_mark_user_timeline_table(self,delta):
        self.con.close()

    def delete_from_mark_user_timeline_table(self):
        self.con.close()

    def create_send_message_timeline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS SEND_MESSAGE_TIMELINE(Id INTEGER PRIMARY KEY AUTOINCREMENT, seconds REAL)")

    def insert_into_send_message_timeline_table(self,delta):
        self.con.close()

    def delete_from_send_message_timeline_table(self):
        self.con.close()

    def create_user_navigation_timeline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS NAVIGATION_TIMELINE(Id INTEGER PRIMARY KEY AUTOINCREMENT, seconds REAL)")

    def insert_into_user_navigation_timeline_table(self,delta):
        self.con.close()

    def delete_from_user_navigation_timeline_table(self):
        self.con.close()

    def create_questionary_editing_timeline_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS QUESTIONATY_EDITING_TIMELINE(Id INTEGER PRIMARY KEY AUTOINCREMENT, seconds REAL)")

    def insert_into_questionary_timeline_table(self,delta):
        self.con.close()

    def delete_from_questionary_timeline_table(self):
        self.con.close()