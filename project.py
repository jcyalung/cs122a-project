# CS 122A Final Project
# requirements
# must contain test_data_project_122a to test folders
#       you can find it in the doc
import sys                              # important for parsing arguments
from args import get_args
from commands import COMMANDS, COMMAND_BOOLS
from constants import COMMAND_ARGS

    
if __name__ == "__main__":
    args = get_args()
    print(args)
    if args["command"] in COMMANDS:
        # Filter args to only include arguments defined for this command
        command_name = args["command"]
        filtered_args = {}
        for arg_def in COMMAND_ARGS[command_name]:
            if arg_def.name in args:
                filtered_args[arg_def.name] = args[arg_def.name]
        result = COMMANDS[command_name](**filtered_args)
        if command_name in COMMAND_BOOLS:
            if result:
                print("Success")
            else:
                print("Fail")
