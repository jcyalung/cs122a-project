import csv
from mysql_helpers import *
from constants import TABLES
import csv
"""
    main function for import command
"""
def importFromFolder(**kwargs):
    folderName = kwargs['folderName']
    print("Dropping tables...")
    for table, types in reversed(list(TABLES.items())):
        if not drop(table):
            print(f"Error dropping table: {table}")
            return False
    print("Successfully dropped tables!")
    
    print("Creating tables...")
    for table, types in TABLES.items():
        if not create_table(table, table_def=types):
            print(f"Error creating table {table}")
            return False
    print("Successfully created tables!")
    
    
    print(f"Importing from folder {folderName}")
    # Define the correct dependency order for importing CSV files
    # Tables must be imported in order to satisfy foreign key constraints
    import_order = [
        "User",                    
        "AgentCreator",            
        "AgentClient",             
        "InternetService",         
        "BaseModel",               
        "LLMService",              
        "DataStorage",             
        "ModelServices",           
        "CustomizedModel",         
        "Configuration",           
        "ModelConfigurations",     
    ]
    
    # Process CSV files in dependency order
    for table_name in import_order:
        csv_file = f"{folderName}/{table_name}.csv"
        try:
            with open(csv_file, 'r') as f:
                csv_reader = csv.reader(f)
                columns = None
                for i, row in enumerate(csv_reader):
                    if i == 0:
                        columns = row
                    else:
                        if not insert(table_name, tuple(columns), tuple(row)):
                            raise Exception(f"Error inserting row into table {table_name}: {row}")
        except FileNotFoundError:
            # Skip if CSV file doesn't exist (optional tables)
            print("Missing file: " + table_name)
            return False
    
    return True

"""
    main function for inserting an agent client
"""
def insertAgentClient(**kwargs):
    uid = kwargs['uid']
    username = kwargs['username']
    email = kwargs['email']
    card_number = kwargs['card_number']
    card_holder = kwargs['card_holder']
    expiration_date = kwargs['expiration_date']
    cvv = kwargs['cvv']
    zip = kwargs['zip']
    interests = kwargs['interests']
    TABLE = "AgentClient"
    # insert into user table (for foreign key)
    user_columns = ('uid', 'email', 'username')
    user_values = (uid, email, username)
    if not insert("User", user_columns, user_values):
        print(f"Failed to insert into User")
        return False
    
    agent_client_columns = ('uid', 'interests', 'cardholder', 'expire', 'cardno', 'cvv', 'zip')
    agent_client_values = (uid, interests, card_holder, expiration_date, card_number, cvv, zip)
    
    if insert(TABLE, agent_client_columns, agent_client_values):
        return True
    else:
        print(f"Failed to insert into {TABLE}")
        return False

def addCustomizedModel(**kwargs):
    mid = kwargs['mid']
    bmid = kwargs['bmid']
    
    customized_model_columns = ('bmid','mid')
    customized_model_values = (bmid, mid)
    TABLE = "CustomizedModel"
    if insert(TABLE, customized_model_columns, customized_model_values):
        return True
    else:
        print(f"Failed to insert into {TABLE}")

def deleteBaseModel(**kwargs):
    # TODO: implement this
    bmid = kwargs['bmid']
    
    if not delete("CustomizedModel", "bmid", bmid):
        print(f"Error deleting related entries in CustomizedModel for bmid {bmid}")
        return False
    
    if delete("BaseModel", "bmid", bmid):
        print(f"Successfully deleted base model {bmid}")
        return True
    else:
        print(f"Failed to delete base model {bmid}")
        return False


def listInternetService(**kwargs):
    bmid = kwargs['bmid']
    query = f"""
        SELECT sid, endpoint, provider
        FROM InternetService
        WHERE bmid = {bmid}
        ORDER BY provider ASC;
    """
    
    result = execute_query(query)
    if result:
        print("sid, endpoint, provider")
        for row in result:
            print(f"{row['sid']}, {row['endpoint']}, {row['provider']}")
        return True
    else:
        print(f"Error retrieving internet services for bmid {bmid}")
        return False

def countCustomizedModel(**kwargs):
    # TODO: implement this
    bmids = kwargs['bmids']
    bmid1, bmid2, bmid3 = bmids
    pass

def topNDurationConfig(**kwargs):
    # TODO: implement this
    uid = kwargs['uid']
    N = kwargs['N']
    pass

def listBaseModelKeyWord(**kwargs):
    # TODO: implement this
    keyword = kwargs['keyword']
    pass

def printNL2SQLresult(**kwargs):
    filename = "NL2SQL_results.csv"
    # Define the order and names of the columns as in the problem description
    header_fields = [
        "NLquery_id",
        "NLquery",
        "LLM_model_name",
        "prompt",
        "LLM_returned_SQL_id",
        "LLM_returned_SQL_query",
        "SQL_correct",
        "SyntaxError",
        "OutputError",
        "TableError"
    ]
    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            print(",".join(header_fields))
            for row in reader:
                output_values = []
                nlquery_id = row.get("NLquery_id","")
                output_values.append(str(nlquery_id) if nlquery_id is not None else "")

                output_values.append(row.get("NLquery", "") if row.get("NLquery", "") is not None else "")
                output_values.append(row.get("LLM_model_name", "") if row.get("LLM_model_name", "") is not None else "")
                output_values.append(row.get("prompt", "") if row.get("prompt", "") is not None else "")

                llm_sql_id = row.get("LLM_returned_SQL_id","")
                output_values.append(str(llm_sql_id) if llm_sql_id is not None else "")

                output_values.append(row.get("LLM_returned_SQL_query", "") if row.get("LLM_returned_SQL_query", "") is not None else "")

                sql_correct_val = row.get("SQL_correct", "")
                output_values.append(sql_correct_val.lower() if sql_correct_val != "" else "")
                for errname in ["SyntaxError", "OutputError", "TableError"]:
                    err_val = row.get(errname, "")
                    output_values.append(err_val.lower() if err_val != "" else "")
                print(",".join(output_values))
        return True
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return False

COMMANDS = {
    "import" : importFromFolder,
    "insertAgentClient" : insertAgentClient,
    "addCustomizedModel" : addCustomizedModel,
    "deleteBaseModel" : deleteBaseModel,
    "listInternetService" : listInternetService,
    "countCustomizedModel" : countCustomizedModel,
    "topNDurationConfig" : topNDurationConfig,
    "listBaseModelKeyWord" : listBaseModelKeyWord,
    "printNL2SQLresult" : printNL2SQLresult,
}