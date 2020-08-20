import argparse
from pathlib import Path

from kivyhelper import lib


def setup_kivy_app_py(app_name: str) -> str:
    """
    Generates a file string for the *App python file in the root kivy
    app.

    Args:
        app_name: A string, the name of the app.

    Returns: A string, the python code to save to the App.py file.

    """
    return (
        "from kivy.app import App\n"
        "from kivy.uix.boxlayout import BoxLayout\n\n\n"
        "class AppFrame(BoxLayout):\n"
        "    pass\n\n\n"
        f"class {app_name}App(App):\n"
        "    def build(self):\n"
        "        return AppFrame()\n\n\n"
        "if __name__ == '__main__':\n"
        f"    {app_name}App().run()\n"
    )


def setup_kivy_app_kv() -> str:
    """
    Generates a file string for the *App kv file in the root kivy app.

    Returns: A string, the kvlang code to save to the App.kv file.

    """
    return (
        "<AppFrame>:\n"
        "    orientation: 'vertical'\n"
    )


def create_new_app(app_name: str, dir_: str):
    """
    Convenience function for creating all the basic python and kv files
    needed by kivy apps.

    Args:
        app_name: A string, the name of the kivy app.
        dir_: A string, the path to the directory to create the new app
            in.

    Returns: None

    """
    d = Path(dir_) if dir_ else Path.cwd()
    lib.print_pycharm_bar()
    print(f'[KIVYHELPER:new_app] Creating Kivy app {app_name} in {d}...')

    app_dir = d.joinpath('game')
    app_dir.mkdir(exist_ok=True)

    print(f'-- Populating {app_dir}')
    print(f'-- Creating {app_name}App.py...')
    app_py = app_dir.joinpath(f'{app_name}App.py')
    app_py.write_text(setup_kivy_app_py(app_name))

    print(f'-- Creating {app_name}.kv...')
    app_py = app_dir.joinpath(f'{app_name}.kv')
    app_py.write_text(setup_kivy_app_kv())
    print('-- App creation complete.')
    lib.print_pycharm_bar()


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


if __name__ == "__main__":
    args = assemble_args()
    create_new_app(args.app_name, args.dir)
