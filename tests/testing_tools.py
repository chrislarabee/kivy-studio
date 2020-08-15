import os
from pathlib import Path

import pytest


class SamplePaths:
    def __init__(self, root: str, **kwargs):
        self.root = Path(root)
        self.input_ = self.root.joinpath(
            kwargs.get('input_'))
        self.input_sprites = self.root.joinpath(
            kwargs.get('input_sprites'))
        self.input_jsons = self.root.joinpath(
            kwargs.get('input_jsons'))
        self.output = self.root.joinpath(
            kwargs.get('output'))


def drop_test_dir(test_dir: str):
    """
    Drops a populated directory.

    Args:
        test_dir: The target directory to drop.

    Returns: None

    """
    print(f'Dropping {test_dir}...')
    for root, dirs, files in os.walk(test_dir, topdown=False):
        for f in files:
            p = Path(root, f)
            print(f'-- Dropping {p}...')
            p.unlink()
        for d in dirs:
            p = Path(root, d)
            print(f'-- Dropping empty dir {p}...')
            p.rmdir()
        p = Path(root)
        print(f'-- Dropping empty dir {p}...')
        p.rmdir()


def check_aseprite() -> bool:
    """
    Attempts to ping aseprite via the command line.

    Returns: True if aseprite responds, False if it does not.

    """
    result = os.system('aseprite --version')
    if result == 1:
        return False
    else:
        return True


def check_aseprite_skip():
    """
    Skips the test it is called in if aseprite is not responsive to
    CLI ping.

    Returns: None

    """
    if not check_aseprite():
        pytest.skip('Aseprite CLI is not being recognized by your system.')
