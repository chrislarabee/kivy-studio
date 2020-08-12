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


def check_aseprite():
    result = os.system('aseprite --version')
    if result == 1:
        return False
    else:
        return True


def check_aseprite_skip():
    if not check_aseprite():
        pytest.skip('Aseprite CLI is not being recognized by your system.')
