#!/usr/bin/env python3

"""Python Base Project
   Copyright (c) YYYY, ...

   Arguments Module

"""

import argparse
import os
import sys

# Support both direct execution and module execution
if __name__ == '__main__' and __package__ is None:
    # Direct execution: add the parent directory to the system path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))
    from baseproject.base import help
else:
    # Module execution (poetry run, etc.)
    from baseproject.base import help


def process_arguments():
    """Processes the arguments given to the program. Returns the parsed
       arguments and the exit code if any error is found. If no error
       is found, the exit code is None."""

    # Prepare the argument parser.
    argument_parser = argparse.ArgumentParser(
        add_help=False, exit_on_error=False)

    # TODO: adapt arguments to your specific needs.
    argument_parser.add_argument("-i", "--input")
    argument_parser.add_argument("-o", "--output")
    argument_parser.add_argument("-v", "--verbose",
                                 action="store_true", default=False)
    argument_parser.add_argument("-h", "--help",
                                 const="none", dest="help_category",
                                 nargs="?", type=str.lower)

    return __parse_arguments(argument_parser)


def __parse_arguments(argument_parser):
    """Parses the program arguments. Returns the parsed arguments and
       the exit code if any error is found. If no error is found, the
       exit code is None."""
    arguments = None
    exit_code = None
    errors = []

    # TODO: adapt parsing to your specific needs.
    try:
        arguments = argument_parser.parse_args()

        # If asking for help, print it and exit.
        if arguments.help_category is not None:
            return None, help.category_help(arguments.help_category)

        # The input file is mandatory and must exist.
        if arguments.input is None:
            errors.append("Missing input file")
            exit_code = 1
        elif not os.path.isfile(arguments.input):
            errors.append("Input file does not exist or is not a file")
            exit_code = 1

        # The output path must not be a directory and must not be the
        # same as the input file. The caller handles overwrite
        # confirmation.
        if arguments.output is None:
            errors.append("Missing output file")
            exit_code = 1
        elif os.path.isdir(arguments.output):
            errors.append("Output file is a directory")
            exit_code = 1
        elif (arguments.input is not None
              and arguments.input == arguments.output):
            errors.append("Input and output files cannot be the same")
            exit_code = 1

    except argparse.ArgumentError as exception:
        errors.append(exception)
        exit_code = 1

    if errors:
        help.help_with_exceptions(errors)
        exit_code = 1

    return arguments, exit_code


if __name__ == '__main__':
    print("BASEP Arguments Module")
