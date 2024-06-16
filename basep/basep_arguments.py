#!/usr/bin/env python3

"""Python Base Project
   Copyright (c) 2024, ...

   Arguments Module

"""

import argparse
import os

from basep import basep_help as bp_hlp


def process_arguments():
    """Processes the arguments given to the program. Returns the parsed
       arguments and the exit code if any error is found. If no error
       is found, exit code is None."""

    # Prepare the argument parser.
    argument_parser = argparse.ArgumentParser(
        add_help=False, exit_on_error=False)

    argument_parser.add_argument("-i", "--input")
    argument_parser.add_argument("-o", "--output")
    argument_parser.add_argument(
        "-h", "--help", const="none", dest="help_category", nargs="?", type=str.lower)

    return __parse_arguments(argument_parser)


def __parse_arguments(argument_parser):
    """Parses the program arguments. Returns the parsed arguments and
       the exit code if any error is found. If no error is found, exit
       code is None."""
    arguments = None
    exit_code = None
    exceptions = []

    # Parse the arguments.
    try:
        arguments = argument_parser.parse_args()

        # If asking for help, print it and exit.
        if arguments.help_category is not None:
            return None, bp_hlp.category_help(arguments.help_category)

        # The input file is mandatory and must exist.
        if arguments.input is None:
            exceptions.append("Missing input file")
            exit_code = 1
        elif not os.path.isfile(arguments.input):
            exceptions.append("Input file does not exist or is not a file")
            exit_code = 1

        # The output file is mandatory. If it exists, it cannot be the
        # same as the input file. Ask whether to overwrite it. The
        # output file cannot be a directory.
        if arguments.output is None:
            exceptions.append("Missing output file")
            exit_code = 1
        elif os.path.isfile(arguments.output):
            if arguments.input == arguments.output:
                exceptions.append("Input and output files cannot be the same")
                exit_code = 1
            else:
                answer = input("Output file already exists, overwrite? [y/N] ")
                if answer.lower() != "y":
                    print()
                    print("Aborting...")
                    return None, 1
                print()
        elif os.path.isdir(arguments.output):
            exceptions.append("Output file is a directory")
            exit_code = 1

    except argparse.ArgumentError as exception:
        exceptions.append(exception)
        exit_code = 1

    if exceptions:
        bp_hlp.help_with_exceptions(exceptions)
        exit_code = 1

    return arguments, exit_code


if __name__ == '__main__':
    print("BASEP Arguments Module")
