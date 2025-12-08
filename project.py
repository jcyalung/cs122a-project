# CS 122A Final Project
# requirements
# must contain test_data_project_122a to test folders
#       you can find it in the doc
import sys                              # important for parsing arguments
from args import get_args
from commands import COMMANDS, COMMAND_BOOLS

    
if __name__ == "__main__":
    args = get_args()
    if args["command"] in COMMANDS:
        result = COMMANDS[args["command"]](**args)
        if args["command"] in COMMAND_BOOLS:
            if result:
                print("Success")
            else:
                print("Fail")
