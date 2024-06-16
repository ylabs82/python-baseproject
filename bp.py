#!/usr/bin/env python3

"""Python Base Project
   Copyright (c) 2024, ...

   Main Module

"""

import sys

from basep import basep_arguments as bp_args
from basep import basep_aux as bp_aux


def main():
    """Program entry point."""

    # Perform initial checks and exit if any error is found.
    checks_result, exit_code = bp_aux.initial_checks()
    if not checks_result:
        sys.exit(exit_code)

    # Parse the arguments and exit if any error is found.
    arguments, exit_code = bp_args.process_arguments()
    if exit_code is not None:
        sys.exit(exit_code)

    # Print the arguments (you can delete this)
    for k in arguments.__dict__:
        print(f"{k}: {arguments.__dict__[k]}")


if __name__ == '__main__':
    main()
