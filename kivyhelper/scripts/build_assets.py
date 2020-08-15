import argparse
import json
import os
import re
from pathlib import Path

from kivyhelper import constants, lib


def assemble_aseprite_cli(
        output_name: str,
        files: list,
        target_dir: str,
        filename_format: str = None) -> str:
    """
    Builds a cli line to execute aseprite's CLI API.

    Args:
        output_name: The name of the desired output png and json files.
        files: A list of the aseprite files to integrate into the png.
        target_dir: The directory to save the resulting png and json to.
        filename_format: A string to be passed to aseprite as the format
            for each frame in the resulting json.

    Returns: A string that is ready to be executed by os.system.

    """
    if not filename_format:
        filename_format = constants.DEFAULT_FF
    td_path = Path(target_dir)
    return (
        f'aseprite -b --ignore-empty --list-tags '
        f'--ignore-layer "Reference Layer 1" '
        f'{" ".join([lib.enquote(f) for f in files])} '
        f'--filename-format {filename_format} '
        f'--sheet {lib.enquote(td_path.joinpath(output_name + ".png"))} '
        f'--data {lib.enquote(td_path.joinpath(output_name + ".json"))}'
    )


def execute_cli_str(cli_str: str):
    """
    Simple function to execute a cli_str. Kept separate primarily to
    ease testing.

    Args:
        cli_str: A string that can be parsed by a cli/bash.

    Returns: None

    """
    os.system(cli_str)


def collect_files(
        input_dir: str,
        ignore: list = None,
        ext: (str, tuple) = None,
        sep: str = '_') -> (dict, tuple):
    """
    Collects file names from the target directory. Will walk all
    subdirectories in the directory.

    Args:
        input_dir: A directory path.
        ignore: A list of regex expressions. Any files with names
            matching any of the expressions will be ignored.
        ext: A string or a tuple of strings, the file extensions to
            collect. If None, will collect all files.
        sep: When creating group keys, names of folders will be
            separated with this string.

    Returns: A dictionary containing parent directories as groups and
        the corresponding list of target files associated with that
        group.

    """
    if ignore:
        ignore_re = re.compile('|'.join(ignore))
    else:
        ignore_re = None
    ext = (ext,) if isinstance(ext, str) else ext
    file_grps = dict()
    input_dir = Path(input_dir)
    subroot_idx = len(input_dir.parts)
    for root, _, files in os.walk(input_dir):
        input_files = []
        root_p = Path(root)
        group = sep.join(root_p.parts[subroot_idx:])
        group = root_p.name if len(group) == 0 else group
        for f in files:
            _, e = os.path.splitext(f)
            if e in ext or ext is None:
                m = ignore_re.match(f) if ignore_re else None
                if not m:
                    input_files.append(str(root_p.joinpath(f)))
        if len(input_files) > 0:
            file_grps[group] = input_files
    return file_grps


def convert_ase_json_to_atlas(j: dict) -> dict:
    """
    Extracts the necessary information from an aseprite json dictionary
    to create a kivy atlas dictionary.

    Args:
        j: A dictionary from an aseprite json.

    Returns: A dictionary containing a single key (the name of the png
        file that j corresponds to), and the frames and their dims from
        that png file.

    """
    return {
        j['meta']['image']: {
            k: [*v['frame'].values()] for k, v in j['frames'].items()
        }
    }


def build_assets_folder(
        input_dir: str,
        output_dir: str,
        ignore: list = None,
        filename_format: str = None,
        sep: str = '_') -> dict:
    """
    Creates an assets folder and populates it with exported aseprite
    file information.

    Args:
        input_dir: A string, the path to the directory to look for
            aseprite files in.
        output_dir: A string, the path to the directory to output png
            and json files into once exported from aseprite.
        ignore: A list of regex expressions, files whose names match
            any of the passed expressions will be ignored.
        filename_format: A string in the aseprite CLI filename-format
            format. Controls how frames are named.
        sep: Will be used as the separator whenever combining file paths
            into strings.

    Returns: A dictionary, the resulting atlas dictionary of the
        aseprite file export.

    """
    d = Path(output_dir).joinpath('assets')
    lib.print_pycharm_bar()
    print(
        f'[KIVYHELPER:build_assets] Creating and populating assets folder in '
        f'{d}...')
    d.mkdir(parents=True, exist_ok=True)
    file_groups = collect_files(
        input_dir, ignore, constants.ASE_EXTS, sep=sep)
    print(f'-- Collected {len(file_groups)} sprite groups.')
    for parent_dir, files in file_groups.items():
        print(f'   > Assembling spritesheet and json for {parent_dir}...')
        cli_str = assemble_aseprite_cli(
            parent_dir,
            files,
            d,
            filename_format
        )
        execute_cli_str(cli_str)
        print(
            f'       ~ Assembled {len(files)} aseprite files into '
            f'{parent_dir}.png')
    print('-- Aseprite exports completed.')
    jsons = collect_files(d, ext='.json')[d.name]

    print(f'-- Collected {len(jsons)} json files resulting from export.')
    atlas = dict()
    print(f'-- Converting json files to atlas files...')
    for file in jsons:
        f = Path(file).stem
        atlas[f] = convert_ase_json_to_atlas(
            lib.read_aseprite_json(file)
        )
        # TODO: Remove aseprite jsons once converted to atlas?
    print(f'-- Json conversions to atlas complete.')
    print(f'-- Writing atlases to {d}...')
    for filename, contents in atlas.items():
        print(f'   > Writing {filename}.atlas...')
        with open(d.joinpath(f'{filename}.atlas'), 'w') as w:
            w.write(json.dumps(contents))
    print(f'-- Write out complete. Build of assets folder complete.')
    lib.print_pycharm_bar()
    return atlas


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


if __name__ == "__main__":
    args = assemble_args()
    build_assets_folder(
        args.input_dir,
        args.output_dir,
        args.ignore,
        args.filename_format
    )
