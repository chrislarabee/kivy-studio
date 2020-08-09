import argparse
import os
import re
from pathlib import Path


def collect_aseprite_files(input_dir: str, ignore: list = None) -> list:
    """
    Collects aseprite file names from the target directory. Will walk
    all subdirectories in the directory.

    Args:
        input_dir: A directory path.
        ignore: A list of regex expressions. Any files with names
            matching any of the expressions will be ignored.

    Returns: A list of strings, paths to the target files.

    """
    if ignore:
        ignore_re = re.compile('|'.join(ignore))
    else:
        ignore_re = None
    input_files = []
    for root, dirs, files in os.walk(input_dir):
        root_p = Path(root)
        for f in files:
            _, ext = os.path.splitext(f)
            if ext in ('.aseprite', 'ase'):
                m = ignore_re.match(f) if ignore_re else None
                if not m:
                    input_files.append(str(root_p.joinpath(f)))
    return input_files


def build_assets_folder(input_dir: str, output_dir: str, ignore: list = None):
    pass



def assemble_args():
    pass