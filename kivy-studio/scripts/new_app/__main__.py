import argparse

from kivyhelper.scripts.new_app.lib import create_new_app


def assemble_args():
    """
    Collects the necessary args for the new_app script.

    Returns: The collected args Namespace.

    """
    parser = argparse.ArgumentParser(
        "Populate a directory with the basics needed for a Kivy app."
    )

    parser.add_argument(
        '--app_name',
        '-a',
        required=True,
        help="The name of the app. Will be used for the Kivy app module "
             "and root kv file."
    )

    parser.add_argument(
        '--dir',
        '-d',
        default=None,
        help="The directory to create the app in. If None, will create "
             "the app in the cwd."
    )

    return parser.parse_args()


args = assemble_args()
create_new_app(args.app_name, args.dir)
