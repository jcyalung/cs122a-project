import mysql.connector

DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="cs122a"
)


def insert(table : str, columns : tuple[str], values : tuple[str]):
    cursor = DB.cursor()