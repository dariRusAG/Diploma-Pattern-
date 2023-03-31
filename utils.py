import sqlite3


def get_db_connection():
    return sqlite3.connect('DB2.sqlite')
