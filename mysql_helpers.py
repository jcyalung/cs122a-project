import mysql.connector

DB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="cs122a"
)

# insert a row into a given table
def insert(tableName : str, columns : tuple[str], values : tuple[str]) -> bool:
    cursor = DB.cursor()
    try:
        placeholders = ", ".join(["%s"] * len(values))
        columns_str = ", ".join([f"`{col}`" for col in columns])
        sql = f"INSERT INTO `{tableName}` ({columns_str}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        DB.commit()
        return True
    except Exception as e:
        print(f"Error inserting into {tableName}: {e}")
        return False
    

# drop the table if exists
def drop(tableName : str) -> bool:
    cursor = DB.cursor()
    try:
        sql = f"DROP TABLE IF EXISTS {tableName}"
        cursor.execute(sql)
        DB.commit()
        return True
    except Exception as e:
        print(f"Error dropping table {tableName}: {e}")
        return False

def create_table(tableName : str, table_def) -> bool:
    try:
        cursor = DB.cursor()
        # Join the list of column definitions with commas
        table_def_str = ", ".join(table_def)
        sql = f"CREATE TABLE IF NOT EXISTS `{tableName}` ({table_def_str})"
        cursor.execute(sql)
        DB.commit()
        return True
    except Exception as e:
        print(f"Error creating table {tableName}: {e}")