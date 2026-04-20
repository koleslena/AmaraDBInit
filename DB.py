import sqlite3 
from sqlite3 import OperationalError

class DB:
    def __init__(self, dbname):
        self.dbname = dbname

    def get_connection(self):
        """Создает соединение с базой данных."""
        return sqlite3.connect(self.dbname)

    def initialize_database(self, filename):
        
        fd = open(filename, 'r')
        sqlFile = fd.read()
        fd.close()

        sqlCommands = sqlFile.split(';')

        conn = self.get_connection()
        cursor = conn.cursor()

        for command in sqlCommands:
            try:
                cursor.execute(command)
            except OperationalError as err:
                print(f"Command skipped: {command}, {err}")

    def insert_rows(self, sqlCommands):

        conn = self.get_connection()
        cursor = conn.cursor()

        for command in sqlCommands:
            try:
                cursor.execute(command)
            except OperationalError as err:
                print(f"Command skipped: {command}, {err}")

        cursor.execute("COMMIT;")

    def get_list(self, table_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        lst = cursor.fetchall()
        conn.close()
        return lst