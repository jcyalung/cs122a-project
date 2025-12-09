import mysql.connector

DB = mysql.connector.connect(
    host="localhost",
    user="test",
    password="password",
    database="cs122a"
)

# insert a row into a given table
def insert(table_name : str, columns : tuple[str], values : tuple[str]) -> bool:
    cursor = DB.cursor()
    try:
        placeholders = ", ".join(["%s"] * len(values))
        columns_str = ", ".join([f"`{col}`" for col in columns])
        sql = f"INSERT INTO `{table_name}` ({columns_str}) VALUES ({placeholders})"
        cursor.execute(sql, values)
        DB.commit()
        return True
    except Exception as e:
        print(f"Error inserting into {table_name}: {e}")
        return False

def delete(table_name : str, column : str, value) -> bool:
    cursor = DB.cursor()
    try:
        check_sql = f"SELECT 1 FROM `{table_name}` WHERE {column} = %s LIMIT 1"
        cursor.execute(check_sql, (value,))
        if cursor.fetchone() is None:
            raise Exception(f"Record with {column} = {value} does not exist in {table_name}")
        sql = f"DELETE FROM `{table_name}` WHERE {column} = %s"
        cursor.execute(sql, (value,))
        DB.commit()
        return True
    except Exception as e:
        print(f"Error deleting from table {table_name}: {e}")
        return False
        

# drop the table if exists
def drop(table_name : str) -> bool:
    cursor = DB.cursor()
    try:
        sql = f"DROP TABLE IF EXISTS {table_name}"
        cursor.execute(sql)
        DB.commit()
        return True
    except Exception as e:
        print(f"Error dropping table {table_name}: {e}")
        return False

# create table with definition
def create_table(table_name : str, table_def) -> bool:
    try:
        cursor = DB.cursor()
        table_def_str = ", ".join(table_def)
        sql = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({table_def_str})"
        cursor.execute(sql)
        DB.commit()
        return True
    except Exception as e:
        print(f"Error creating table {table_name}: {e}")
        
def select(table_name: str, column: str, value):
    cursor = DB.cursor()
    try:
        sql = f"SELECT * FROM `{table_name}` WHERE {column} = %s"
        cursor.execute(sql, (value,))
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Error selecting from table {table_name}: {e}")
        return None

def execute_custom_select(sql : str, value : str=None):
    cursor = DB.cursor()
    try:
        result = None
        if value:
            cursor.execute(sql, (value,))
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error selecting: {e}")
        return False

def execute_custom_select_multi(sql : str, values : tuple=None):
    cursor = DB.cursor()
    try:
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error selecting: {e}")
        return False