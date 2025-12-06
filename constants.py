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
    def __init__(self, name : str, type : type, help : str) -> None:
        self.name = name
        self.type = type
        self.help = help
        
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
        Argument('bmid1', int, 'bmid1 of list'),
        Argument('bmid2', int, 'bmid2 of list'),
        Argument('bmid3', int, 'bmid3 of list'),
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