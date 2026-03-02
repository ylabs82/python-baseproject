#!/usr/bin/env python3

"""Python Base Project
   Copyright (c) 2026, ...

   Main Module

"""

import logging
import os
import sys

# Support both direct execution and module execution
if __name__ == '__main__' and __package__ is None:
    # Direct execution: add the parent directory to the system path
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    from baseproject.base import arguments as args, helpers
else:
    # Module execution (poetry run, etc.)
    from baseproject.base import arguments as args, helpers


class BaseProject:
    def __init__(self):
        pass

    def main(self):
        """Program entry point."""

        # Perform initial checks and exit if any error is found.
        checks_result, exit_code = helpers.initial_checks()
        if not checks_result:
            sys.exit(exit_code)

        # Parse the arguments and exit if any error is found.
        arguments, exit_code = args.process_arguments()
        if exit_code is not None:
            sys.exit(exit_code)

        # TODO: from this point, replace with your business logic.
        # Configure logging based on the --verbose flag.
        logging.basicConfig(
            level=logging.DEBUG if arguments.verbose
            else logging.WARNING,
            format="%(levelname)s: %(message)s"
        )

        # Confirm overwriting if the output file already exists.
        if os.path.isfile(arguments.output):
            if not helpers.confirm_overwrite(arguments.output):
                logging.debug("Do not overwrite '%s'. Aborting.",
                              arguments.output)
                print("Aborting...")
                sys.exit(1)

        for k in arguments.__dict__:
            print(f"{k}: {arguments.__dict__[k]}")


def main():
    base_project = BaseProject()
    base_project.main()


if __name__ == '__main__':
    main()
