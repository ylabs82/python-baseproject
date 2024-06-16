#!/usr/bin/env python3

"""Python Base Project
   Copyright (c) 2024, ...

   Help Module

"""

from basep import basep_consts as bp_c

CATEGORY_PLACEHOLDER_1 = """\
CATEGORY_PLACEHOLDER_1
"""

CATEGORY_PLACEHOLDER_2 = """\
CATEGORY_PLACEHOLDER_2
"""


def basic_help():
    """Prints the program usage."""
    __help_title()
    __help_body()
    __help_footer()


def category_help(category):
    """Prints the help of the given category. Returns 0 if the category is
       valid, 1 otherwise."""
    toret = 0

    if category == "none":
        basic_help()
    elif category == "category":
        __help_title()
        __show_categories()
    elif category == "category_placeholder_1":
        __help_title()
        print(CATEGORY_PLACEHOLDER_1)
    elif category == "category_placeholder_2":
        __help_title()
        print(CATEGORY_PLACEHOLDER_2)
    else:
        __help_title()
        print(" Invalid help category")
        toret = 1

    return toret


def help_with_exceptions(exceptions_messages):
    """Prints the help of the program with the given exception
       messages. Returns nothing."""
    __help_title()

    # Print the exception messages.
    for exception_message in exceptions_messages:
        print(exception_message)
    print()

    __help_body()


def __help_title():
    """Prints the title of the help. Returns nothing."""
    print(f"{bp_c.PROG_NAME}, v{bp_c.PROG_VERSION}")
    print(f"Copyright (c) {bp_c.PROG_YEAR}, {bp_c.PROG_COMPANY}")
    print("Original author: ...")
    print()


def __help_body():
    """Prints the body of the help. Returns nothing."""
    print(f"Usage: {bp_c.EXECUTABLE} [options...]")
    print(" * -i, --input <input file>    Input file")
    print(" * -o, --output <output file>  Output file")
    print("   -h, --help <category>       Get full help")


def __help_footer():
    """Prints the footer of the help. Returns nothing."""
    print()
    print("This is not the full help, use \"--help category\" to get a list of")
    print("all categories.")


def __show_categories():
    """Prints the help categories. Returns nothing."""
    print(" category_placeholder_1  Get info about first category")
    print(" category_placeholder_2  Get info about second category")
    print()


if __name__ == '__main__':
    print("BASEP Help Module")
