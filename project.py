# CS 122A Final Project
# requirements
# must contain test_data_project_122a to test folders
#       you can find it in the doc
import mysql_helper as db
import sys                              # important for parsing arguments

def dummy():
    pass


# commands that we have to fill
# any command that has the function "dummy" is not implemented yet
COMMANDS = {
    "import"                : dummy,
    "insertAgentClient"     : dummy,
    "addCustomizedModel"    : dummy,
    "deleteBaseModel"       : dummy,
    "listInternetService"   : dummy,
    "countCustomizedModel"  : dummy,
    "topNDurationConfig"    : dummy,
    "listBaseModelKeyWord"  : dummy,
    
    # experiment/extra credit?
    "printNL2SQLresult"     : dummy,
}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(sys.argv)