from datetime import datetime


def dummy(): pass


# all the names of the commands
COMMANDS = {
    "import",
    "insertAgentClient",
    "addCustomizedModel",
    "deleteBaseModel",
    "listInternetService",
    "countCustomizedModel",
    "topNDurationConfig",
    "listBaseModelKeyWord",
    "printNL2SQLresult",
}


# descriptions of the commands
COMMAND_DESCRIPTIONS = {
    "import" :                  "Create new tables from folder",
    "insertAgentClient" :       "Insert a new Agent Client into the related tables",
    "addCustomizedModel" :      "Add a new customized model to the tables",
    "deleteBaseModel" :         "Delete a base model from the tables",
    "listInternetService" :     "Given a base model id, list all the internet services that the model is utilizing, sorted by provider's name in ascending order",
    "countCustomizedModel" :    "Given a list of base model id, for each base model id, count on the numbers of customized models that build from it in ascending order",
    "topNDurationConfig"   :    "Given an agent client id, list the top-N longest duration configurations with longest duration, in descending order",
    "listBaseModelKeyWord" :    "List 5 base models that are utilizing LLM services whose domain contains the keyword “video” in ascending order",
    "printNL2SQLresult":        "NL2SQL Credit",
}


class Argument():
    def __init__(self, name : str, type : type, help : str, nargs = 1) -> None:
        self.name = name
        self.type = type
        self.help = help
        self.nargs = nargs
        
# handles the arguments of commands, type -h to help
COMMAND_ARGS = {
    "import"                 : [
        Argument('folderName', str, "Folder containing CSV files")
    ],
    "insertAgentClient"     : [
        Argument('uid', int, "UID of agent"),
        Argument('username', str, "Username of agent"),
        Argument('email', str, "Email of client"),
        Argument('card_number', int, "Card number of client"),
        Argument('card_holder', str, "Card holder of client"),
        Argument('expiration_date', str, "Expiration date of card"),
        Argument('cvv', int, "CVV of card"),
        Argument('zip', int, "Zipcode of card"),
        Argument('interests', str, "Personal interests"),
    ],
    "addCustomizedModel"    : [
        Argument('mid', int, 'mid of model'),
        Argument('bmid', int, 'bmid of model'),
    ],
    "deleteBaseModel"       : [
        Argument('bmid', int, 'bmid of model to delete'),
    ],
    "listInternetService"   : [
        Argument('bmid', int, 'bmid of model to list'),
    ],
    "countCustomizedModel"  : [
        Argument('bmids', int, 'list of bmids (>=1)', nargs='+'),
    ],
    "topNDurationConfig"    : [
        Argument('uid', int, 'uid of agent client'),
        Argument('N', int, 'top N longest duration configurations'),
    ],
    "listBaseModelKeyWord"  : [
        Argument('keyword', str, "keyword to search")
    ],
    "printNL2SQLresult"     : [],
}

TABLES = {
    "User": [
        "uid INT",
        "email TEXT NOT NULL",
        "username TEXT NOT NULL",
        "PRIMARY KEY (uid)"
    ],
    "AgentCreator": [
        "uid INT",
        "bio TEXT",
        "payout TEXT",
        "PRIMARY KEY (uid)",
        "FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE"
    ],
    "AgentClient": [
        "uid INT",
        "interests TEXT NOT NULL",
        "cardholder TEXT NOT NULL",
        "expire DATE NOT NULL",
        "cardno BIGINT NOT NULL",
        "cvv INT NOT NULL",
        "zip INT NOT NULL",
        "PRIMARY KEY (uid)",
        "FOREIGN KEY (uid) REFERENCES User(uid) ON DELETE CASCADE"
    ],
    "BaseModel": [
        "bmid INT",
        "creator_uid INT NOT NULL",
        "description TEXT NOT NULL",
        "PRIMARY KEY (bmid)",
        "FOREIGN KEY (creator_uid) REFERENCES AgentCreator(uid) ON DELETE CASCADE"
    ],
    "CustomizedModel": [
        "bmid INT",
        "mid INT NOT NULL",
        "PRIMARY KEY (bmid, mid)",
        "FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE"
    ],
    "Configuration": [
        "cid INT",
        "client_uid INT NOT NULL",
        "content TEXT NOT NULL",
        "labels TEXT NOT NULL",
        "PRIMARY KEY (cid)",
        "FOREIGN KEY (client_uid) REFERENCES AgentClient(uid) ON DELETE CASCADE"
    ],
    "InternetService": [
        "sid INT",
        "provider TEXT NOT NULL",
        "endpoints TEXT NOT NULL",
        "PRIMARY KEY (sid)"
    ],
    "LLMService": [
        "sid INT",
        "domain TEXT",
        "PRIMARY KEY (sid)",
        "FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE"
    ],
    "DataStorage": [
        "sid INT",
        "type TEXT",
        "PRIMARY KEY (sid)",
        "FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE"
    ],
    "ModelServices": [
        "bmid INT NOT NULL",
        "sid INT NOT NULL",
        "version INT NOT NULL",
        "PRIMARY KEY (bmid, sid)",
        "FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE",
        "FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE"
    ],
    "ModelConfigurations": [
        "bmid INT NOT NULL",
        "mid INT NOT NULL",
        "cid INT NOT NULL",
        "duration INT NOT NULL",
        "PRIMARY KEY (bmid, mid, cid)",
        "FOREIGN KEY (bmid, mid) REFERENCES CustomizedModel(bmid, mid) ON DELETE CASCADE",
        "FOREIGN KEY (cid) REFERENCES Configuration(cid) ON DELETE CASCADE"
    ]
}

def get_internet_services_for_model(bmid):
    """
    Given a base model id, list all the internet services that the model is utilizing,
    sorted by provider's name in ascending order.

    Args:
        bmid (int): The base model id.

    Returns:
        list of dict: Each dict contains 'sid', 'provider', and 'endpoints' for an InternetService.
    """
    from mysql_helpers import DB
    cursor = DB.cursor(dictionary=True)
    sql = """
        SELECT isrv.sid, isrv.provider, isrv.endpoints
        FROM ModelServices ms
        JOIN InternetService isrv ON ms.sid = isrv.sid
        WHERE ms.bmid = %s
        ORDER BY isrv.provider ASC
    """
    try:
        cursor.execute(sql, (bmid,))
        services = cursor.fetchall()
        return services
    except Exception as e:
        print(f"Error retrieving internet services for bmid={bmid}: {e}")
        return []
