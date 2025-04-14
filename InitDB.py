import sqlite3 
from sqlite3 import OperationalError

def get_connection():
    """Создает соединение с базой данных."""
    return sqlite3.connect('amara.db')

def initialize_database(filename):
    
    fd = open(filename, 'r')
    sqlFile = fd.read()
    fd.close()

    sqlCommands = sqlFile.split(';')

    conn = get_connection()
    cursor = conn.cursor()

    for command in sqlCommands:
        try:
            cursor.execute(command)
        except OperationalError as err:
            print(f"Command skipped: {command}, {err}")

def insert_rows(sqlCommands):

    conn = get_connection()
    cursor = conn.cursor()

    for command in sqlCommands:
        try:
            cursor.execute(command)
        except OperationalError as err:
            print(f"Command skipped: {command}, {err}")

    cursor.execute("COMMIT;")

def get_list(table_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    lst = cursor.fetchall()
    conn.close()
    return lst