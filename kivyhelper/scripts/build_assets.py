import argparse
import os
import re
from pathlib import Path

from kivyhelper import constants


def assemble_aseprite_cli(
        output_name: str,
        files: list,
        target_dir: str,
        filename_format: str = None):
    if not filename_format:
        filename_format = '{title}_{tag}_{tagframe}'
    td_path = Path(target_dir)
    return (
        f"aseprite -b --ignore-empty --list-tags "
        f"--ignore-layer 'Reference Layer 1' "
        f"{' '.join(files)} "
        f"--filename-format {filename_format} "
        f"--sheet {td_path.joinpath(output_name + '.png')} "
        f"--data {td_path.joinpath(output_name + '.json')}"
    )


def execute_aseprite_cli(cli_str: str):
    os.system(cli_str)


def collect_files(
        input_dir: str,
        ignore: list = None,
        ext: (str, tuple) = None) -> dict:
    """
    Collects file names from the target directory. Will walk all
    subdirectories in the directory.

    Args:
        input_dir: A directory path.
        ignore: A list of regex expressions. Any files with names
            matching any of the expressions will be ignored.
        ext: A string or a tuple of strings, the file extensions to
            collect. If None, will collect all files.

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
        group = ''.join(root_p.parts[subroot_idx:])
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


def build_assets_folder(input_dir: str, output_dir: str, ignore: list = None):
    files = collect_files(input_dir, ignore, constants.ASE_EXTS)




def assemble_args():
    pass