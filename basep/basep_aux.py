#!/usr/bin/env python3

"""Python Base Project
   Copyright (c) 2024, ...

   Auxiliary Module

"""

import os
import shutil
import sys

from basep import basep_help as bp_hlp


def initial_checks():
    """Performs the initial checks for the program. Returns a tuple with the
       result of the checks and the exit code if the checks fail."""
    checks_results = True
    exit_code = None

    # If no arguments are provided, print usage.
    if len(sys.argv) == 1:
        bp_hlp.basic_help()
        checks_results = False
        exit_code = 1

    # Check if needed programs are installed.
    elif not __exists_commands("", ""):
        bp_hlp.help_with_exceptions(
            ["This program needs the following programs to function properly:" +
             os.linesep + " - ..." +
             os.linesep + " - ..." +
             os.linesep +
             os.linesep + "Please, make sure you have installed these programs and try again."])
        checks_results = False
        exit_code = 1

    return checks_results, exit_code


def __exists_commands(*commands):
    """Checks whether the given commands exist in the system. Returns True if
       all the commands exists, False otherwise."""
    toret = True

    for command in commands:
        if command != "" and command is not None:
            toret = toret and shutil.which(command) is not None
            if not toret:
                break

    return toret


if __name__ == '__main__':
    print("BASEP Auxiliary Module")
