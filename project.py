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


"""

test_keywordSearch
Test Failed: ('Incorrect Results: ', "['project.py', 'listBaseModelKeyWord', 'video']\n8\n17\n19\n")

test_listService
Test Failed: ('Incorrect Results: ', "['project.py', 'listInternetService', '17']\n9,Google,https://google2.example.com/v1;https://google3.example.com/v1\n3,OpenAI,https://openai1.example.com/v1\n")

test_topConfig1
Test Failed: ('Incorrect Results: ', "['project.py', 'topNDurationConfig', '20', '2']\n")

test_topConfig2
Test Failed: ('Incorrect Results: ', "['project.py', 'topNDurationConfig', '10', '3']\n")

"""