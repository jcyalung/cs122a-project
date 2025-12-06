import mysql.connector

try:
    DB = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
    )
except Exception as e:
    raise e

def insert(table : str, columns : tuple[str], values : tuple[str]):
    pass