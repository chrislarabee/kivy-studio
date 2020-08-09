import argparse
from pathlib import Path


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
        "from kivy.uix.floatlayout import FloatLayout\n\n\n"
        "class AppFrame(FloatLayout):\n"
        "    pass\n\n\n"
        f"class {app_name}App(App):\n"
        "    def build(self):\n"
        "        return AppFrame()\n\n\n"
        "if __name__ == '__main__':\n"
        f"    {app_name}App().run()\n"
    )


def create_new_app(app_name: str, dir_: str):
    d = Path(args.dir) if dir_ else Path.cwd()
    print(f'[KIVYHELPER:new_app] Creating Kivy app {app_name} in {d}...')

    app_dir = d.joinpath(app_name)
    app_dir.mkdir(exist_ok=True)

    print(f'-- Creating {app_name}App.py in {app_dir}...')
    app_py = app_dir.joinpath(f'{app_name}App.py')
    app_py.write_text(setup_kivy_app_py(app_name))


if __name__ == "__main__":
    args = assemble_args()
    create_new_app(args.app_name, args.dir)
