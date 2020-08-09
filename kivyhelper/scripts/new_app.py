import argparse
import os


def assemble_args():
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


def execute():
    args = assemble_args()

    d = args.dir if args.dir else os.getcwd()

    print(f'[KIVYHELPER:new_app] Creating Kivy app {args.app_name} in {d}...')


if __name__ == "__main__":
    execute()
