# CS 122A Final Project
# requirements
# must contain test_data_project_122a to test folders
#       you can find it in the doc
import sys                              # important for parsing arguments
from args import get_args
from commands import COMMANDS

    
if __name__ == "__main__":
    args = get_args()
    if args["command"] in COMMANDS:
        result = COMMANDS[args["command"]](**args)
    else:
        raise Exception(f"Unknown command {args.command}")
        
    