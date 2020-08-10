import warnings
from pathlib import Path

import pytest

from tests import testing_tools


@pytest.fixture(scope='session', autouse=True)
def aseprite():
    aseprite_resp = testing_tools.check_aseprite()
    if not aseprite_resp:
        warnings.warn(
            'Aseprite is not responding to CLI commands. This means '
            'that the tests related to interacting with the Aseprite '
            'CLI will be skipped. See the README for info on how to set '
            'up Aseprite CLI.'
        )


@pytest.fixture(scope='session', autouse=True)
def output_data():
    Path('tests/test_data/output').mkdir(exist_ok=True)


@pytest.fixture
def sprite_files():
    return {
        'sprites': [
            'tests\\test_data\\input\\sprites\\ignore_sprite.aseprite',
            'tests\\test_data\\input\\sprites\\test_sprite.aseprite',
            'tests\\test_data\\input\\sprites\\test_sprite2.aseprite',
        ],
        'spritessprite_subdir': [
            'tests\\test_data\\input\\sprites\\sprite_subdir\\test_subsprite.aseprite',
        ]
    }


@pytest.fixture
def aseprite_cli(sprite_files):
    return (
        "aseprite -b --ignore-empty --list-tags "
        f"{sprite_files['sprites'][0]} "
        f"{sprite_files['sprites'][1]} "
        f"{sprite_files['sprites'][2]} "
        "--sheet tests/test_data/output/sprites.png "
        "--data tests/test_data/output/sprites.json"
    )
