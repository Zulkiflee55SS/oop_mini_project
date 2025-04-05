import mysql.connector

class DatabaseManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="parttime_db"
        )
        self.cursor = self.connection.cursor()

    def fetch_all(self, query, params=None):
        self.cursor.execute(query, params) 
        return self.cursor.fetchall() 


    def execute(self, query, params=None):

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit() 

    def close(self):
        self.cursor.close()
        self.connection.close()
