#!/usr/bin/env python3

"""Python Base Project
   Copyright (c) 2026, ...

   Helpers Module

"""

import os
import shutil
import sys

# Support both direct execution and module execution
if __name__ == '__main__' and __package__ is None:
    # Direct execution: add the parent directory to the system path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
    from baseproject.base import consts as c, help
else:
    # Module execution (poetry run, etc.)
    from baseproject.base import consts as c, help


def confirm_overwrite(output_path):
    """Asks the user to confirm overwriting an existing output file.
       Returns True if the user confirms, False otherwise."""
    answer = input(
        f"Output file '{output_path}' already exists, overwrite? [y/N] ")
    print()
    return answer.lower() == "y"


def initial_checks():
    """Performs the initial checks for the program. Returns a tuple with the
       result of the checks and the exit code if the checks fail."""
    checks_results = True
    exit_code = None

    # If no arguments are provided, print usage.
    if len(sys.argv) == 1:
        help.basic_help()
        checks_results = False
        exit_code = 1

    # Check if the required commands are installed.
    elif not __exists_commands(c.COMMANDS_REQUIRED):
        commands_required_list = ""
        for command in c.COMMANDS_REQUIRED:
            commands_required_list = (
                    commands_required_list +
                    os.linesep +
                    " - " + command
            )

        help.help_with_exceptions(
            ["This program needs the following command(s) to function " +
             "properly:" +
             commands_required_list +
             os.linesep +
             os.linesep + "Please, make sure you have these commands " +
             "installed and try again."])
        checks_results = False
        exit_code = 1

    return checks_results, exit_code


def __exists_commands(commands):
    """Checks whether the given commands exist in the system. Returns
       True if all the commands exist, False otherwise."""
    toret = True

    for command in commands:
        if command != "" and command is not None:
            toret = toret and shutil.which(command) is not None
            if not toret:
                break

    return toret


if __name__ == '__main__':
    print("BASEP Helpers Module")
