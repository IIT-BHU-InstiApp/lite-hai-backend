import argparse

import django
django.setup()

# pylint: disable=wrong-import-position
from .populate_database import populate_database

_PARSER = argparse.ArgumentParser(description="""
Some scripts for development purposes only.
""")

_PARSER.add_argument(
    '--populate_db',
    help='Populates the database with values used during testing.',
    action='store_true')


def main(args=None):
    """
    Main function for this module
    """
    parsed_args = _PARSER.parse_args(args=args)

    if parsed_args.populate_db:
        populate_database()
        print("Successfully loaded test database.")


if __name__ == '__main__':
    main()
