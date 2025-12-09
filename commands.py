import csv
from mysql_helpers import *
from constants import TABLES
import csv
"""
    main function for import command
"""
def importFromFolder(**kwargs):
    folderName = kwargs['folderName']
    for table, types in reversed(list(TABLES.items())):
        if not drop(table):
            return False
    
    for table, types in TABLES.items():
        if not create_table(table, table_def=types):
            print(f"Error creating table {table}")
            return False
    
    
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
    user_columns = ('uid', 'email', 'username')
    user_values = (uid, email, username)
    if not insert("User", user_columns, user_values):
        return False
    
    agent_client_columns = ('uid', 'interests', 'cardholder', 'expire', 'cardno', 'cvv', 'zip')
    agent_client_values = (uid, interests, card_holder, expiration_date, card_number, cvv, zip)
    
    return insert(TABLE, agent_client_columns, agent_client_values)

def addCustomizedModel(**kwargs):
    mid = kwargs['mid']
    bmid = kwargs['bmid']
    
    base_model_results = select("BaseModel", "bmid", bmid)
    if base_model_results is None or len(base_model_results) == 0:
        # print(f"Error inserting into CustomizedModel: BaseModel with bmid={bmid} does not exist")
        return False
    
    customized_model_columns = ('bmid','mid')
    customized_model_values = (bmid, mid)
    TABLE = "CustomizedModel"
    return insert(TABLE, customized_model_columns, customized_model_values)

def deleteBaseModel(**kwargs):
    bmid = kwargs['bmid']
    COLUMN = 'bmid'
    TABLE = "BaseModel"
    return delete(TABLE, COLUMN, bmid)
        
def listInternetService(**kwargs):
    bmid = kwargs['bmid']
    sql = sql = """
        SELECT isrv.sid, isrv.provider, isrv.endpoints
        FROM ModelServices ms
        JOIN InternetService isrv ON ms.sid = isrv.sid
        WHERE ms.bmid = %s
        ORDER BY isrv.provider ASC
    """
    results = execute_custom_select(sql, bmid)
    if results is False or results is None or len(results) == 0:
        print("Fail")
        return False
    for row in results:
        sid, provider, endpoints = row
        print(f"{sid},{provider},{endpoints}")
    return True

def countCustomizedModel(**kwargs):
    bmids = kwargs['bmids']
    # Ensure bmids is a list (argparse with nargs='+' returns a list)
    if not isinstance(bmids, list):
        bmids = [bmids]
    
    if len(bmids) == 0:
        return False
    
    # Build SQL query with dynamic number of placeholders
    placeholders = ', '.join(['%s'] * len(bmids))
    sql = f"""
        SELECT bm.bmid, bm.description, COUNT(cm.mid) as customizedModelCount
        FROM BaseModel bm
        LEFT JOIN CustomizedModel cm ON bm.bmid = cm.bmid
        WHERE bm.bmid IN ({placeholders})
        GROUP BY bm.bmid, bm.description
        ORDER BY bm.bmid ASC
    """
    results = execute_custom_select_multi(sql, tuple(bmids))
    if results is False:
        return False
    
    counts = {bmid: 0 for bmid in bmids}
    descriptions = {}
    
    for row in results:
        bmid, description, count = row
        counts[bmid] = count
        descriptions[bmid] = description
    
    for bmid in bmids:
        if bmid not in descriptions:
            base_model_results = select("BaseModel", "bmid", bmid)
            if base_model_results and len(base_model_results) > 0:
                descriptions[bmid] = base_model_results[0][2]
            else:
                descriptions[bmid] = ""
    
    for bmid in sorted(counts.keys()):
        description = descriptions.get(bmid, "")
        print(f"{bmid},{description},{counts[bmid]}")
    
    return True

def topNDurationConfig(**kwargs):
    uid = kwargs['uid']
    N = kwargs['N']
    
    if isinstance(uid, list):
        uid = uid[0]
    if isinstance(N, list):
        N = N[0]
    
    uid = int(uid)
    N = int(N)
    
    sql = """
        SELECT mc.bmid, mc.mid, mc.cid, mc.duration
        FROM ModelConfigurations mc
        JOIN CustomizedModel cm ON mc.bmid = cm.bmid AND mc.mid = cm.mid
        JOIN BaseModel bm ON cm.bmid = bm.bmid
        WHERE bm.creator_uid = %s
        ORDER BY mc.duration DESC
        LIMIT %s
    """
    results = execute_custom_select_multi(sql, (uid, N))
    if results is False:
        return False
    if not results:
        return True
    for row in results:
        bmid, mid, cid, duration = row
        print(f"{bmid},{mid},{cid},{duration}")
    return True

def listBaseModelKeyWord(**kwargs):
    keyword = kwargs['keyword']
    
    sql = """
        SELECT DISTINCT bm.bmid
        FROM BaseModel bm
        JOIN ModelServices ms ON bm.bmid = ms.bmid
        JOIN LLMService llm ON ms.sid = llm.sid
        WHERE llm.domain IS NOT NULL AND LOWER(llm.domain) LIKE LOWER(%s)
        ORDER BY bm.bmid ASC
        LIMIT 5
    """
    keyword_pattern = f"%{keyword}%"
    results = execute_custom_select(sql, keyword_pattern)
    if results is False:
        print("Fail")
        return False
    if results is None or len(results) == 0:
        print("Fail")
        return False
    for row in results:
        bmid = row[0]
        print(f"{bmid}")
    return True

def printNL2SQLresult(**kwargs):
    filename = "NL2SQL_results.csv"
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

COMMAND_BOOLS = {
    "import",
    "insertAgentClient",
    "addCustomizedModel",
    "deleteBaseModel",
}