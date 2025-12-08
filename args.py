# responsible to setting up the arguments
# commands that we have to fill
# any command that has the function "dummy" is not implemented yet
from argparse import ArgumentParser
from constants import COMMAND_ARGS, COMMAND_DESCRIPTIONS
parser = ArgumentParser(description="CLI Project for CS 122A.")



def config() -> ArgumentParser:
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    for name, description in COMMAND_DESCRIPTIONS.items():
        current = subparsers.add_parser(name=name, description=description)
        for arg in COMMAND_ARGS[name]:
            if arg.nargs > 1:
                current.add_argument(arg.name, type=arg.type, help=arg.help, nargs=arg.nargs)
            else:
                current.add_argument(arg.name, type=arg.type, help=arg.help)
                

def get_args():
    config()
    args = parser.parse_args()
    if args.command == None:
        parser.print_help()
    return vars(args)