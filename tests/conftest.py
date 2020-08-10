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
def aseprite_json():
    return {
        "frames": {
            "test_sprite 0.aseprite": {
                "frame": {"x": 0, "y": 32, "w": 32, "h": 32},
                "rotated": False,
                "trimmed": False,
                "spriteSourceSize": {"x": 0, "y": 0, "w": 32, "h": 32},
                "sourceSize": {"w": 32, "h": 32},
                "duration": 100
            },
            "test_sprite 1.aseprite": {
                "frame": {"x": 32, "y": 32, "w": 32, "h": 32},
                "rotated": False,
                "trimmed": False,
                "spriteSourceSize": {"x": 0, "y": 0, "w": 32, "h": 32},
                "sourceSize": {"w": 32, "h": 32},
                "duration": 100
               }
        },
        "meta": {
            "app": "http://www.aseprite.org/",
            "version": "1.2.21",
            "image": "sprites.png",
            "format": "RGBA8888",
            "size": {"w": 64, "h": 32},
            "scale": "1",
            "frameTags": [
                {"name": "Start", "from": 0, "to": 1, "direction": "forward"},
            ]
        }
    }


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
        f"--ignore-layer 'Reference Layer 1' "
        f"{sprite_files['sprites'][0]} "
        f"{sprite_files['sprites'][1]} "
        f"{sprite_files['sprites'][2]} "
        "--sheet tests/test_data/output/sprites.png "
        "--data tests/test_data/output/sprites.json"
    )
