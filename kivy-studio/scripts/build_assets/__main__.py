import argparse

from kivyhelper import constants
from kivyhelper.scripts.build_assets.lib import build_assets_folder


def assemble_args():
    parser = argparse.ArgumentParser(
        "Populate an assets folder from Aseprite files. Creates "
        "spritesheets and an atlas file."
    )

    parser.add_argument(
        '--input_dir',
        '-i',
        required=True,
        help='The path to the directory containing the desired aseprite '
             'files to export.'
    )

    parser.add_argument(
        '--output_dir',
        '-o',
        required=True,
        help='The path to the directory to export to.'
    )

    parser.add_argument(
        '--ignore',
        nargs='*',
        help='A list of regex expressions indicating files to ignore. '
             'Files whose names match any of the expressions will be '
             'ignored.'
    )

    parser.add_argument(
        '--filename_format',
        '-ff',
        help='The aseprite format to use for the key corresponding to '
             'each frame when exporting aseprite files. Default is '
             f'{constants.DEFAULT_FF}'
    )

    return parser.parse_args()


args = assemble_args()
build_assets_folder(
    args.input_dir,
    args.output_dir,
    args.ignore,
    args.filename_format
)
