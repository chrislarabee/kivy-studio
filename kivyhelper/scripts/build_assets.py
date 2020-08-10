import argparse
import os
import re
from pathlib import Path


def assemble_aseprite_cli(output_name: str, files: list, target_dir: str):
    return (
        f"aseprite -b --ignore-empty --list-tags "
        f"--ignore-layer 'Reference Layer 1' "
        f"{' '.join(files)} "
        f"--sheet {target_dir}/{output_name}.png "
        f"--data {target_dir}/{output_name}.json"
    )


def execute_aseprite_cli(cli_str: str):
    os.system(cli_str)


def collect_aseprite_files(input_dir: str, ignore: list = None) -> dict:
    """
    Collects aseprite file names from the target directory. Will walk
    all subdirectories in the directory.

    Args:
        input_dir: A directory path.
        ignore: A list of regex expressions. Any files with names
            matching any of the expressions will be ignored.

    Returns: A dictionary containing parent directories as groups and
        the corresponding list of target files associated with that
        group.

    """
    if ignore:
        ignore_re = re.compile('|'.join(ignore))
    else:
        ignore_re = None
    spritesheet_grps = dict()
    input_dir = Path(input_dir)
    subroot_idx = len(input_dir.parts)
    for root, _, files in os.walk(input_dir):
        input_files = []
        root_p = Path(root)
        group = ''.join(root_p.parts[subroot_idx:])
        group = root_p.name if len(group) == 0 else group
        for f in files:
            _, ext = os.path.splitext(f)
            if ext in ('.aseprite', '.ase'):
                m = ignore_re.match(f) if ignore_re else None
                if not m:
                    input_files.append(str(root_p.joinpath(f)))
        if len(input_files) > 0:
            spritesheet_grps[group] = input_files
    return spritesheet_grps


def build_assets_folder(input_dir: str, output_dir: str, ignore: list = None):
    files = collect_aseprite_files(input_dir, ignore)




def assemble_args():
    pass