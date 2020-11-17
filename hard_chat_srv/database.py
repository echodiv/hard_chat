import logging
import time
import json
import sqlite3

# dep
class Database():
    def __init__(self):
        ''' Class for working with database '''
        self.host = 'localhost'
        self.port = 3306
        self.user = 'root'
        self.password = 'pwd'
        self.db_name = 'hard_chat_db'
        self.con = None
        self.cursor = None

    def configure(self, host, port, user, password):
        ''' Configure connection to Database
    
        @attributes
        host - web host
        post - database port fo connection
        user - database user (SCHEMA) name
        password - password for database user
        '''
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
        ''' Connect to database 
        '''
        #self.cursor = MySQLdb.connect(host = self.host,
        #                              user = self.user,
        #                              passwd = self.password,
        #                              db = self.db_name)
        try:
            self.con = sqlite3.connect(self.db_name)
            self.cursor = self.con.cursor()
            #log SUCCESS
        except sqlite3.Error as error:
            #log Error
            a = 2

    def disconnect(self):
        if not self.con:
            raise Exception("No connection to database")
        self.con.disconnect()

    def message_write(self):
        '''docString '''   
        pass

    def message_read(self):
        '''docString '''
        pass 


def __unit():
    db = Database()
    db.connect()
    assert db.cursor, 'Connection error'
    

if __name__ == '__main__':
    __unit()
