import warnings
from argparse import Namespace
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


@pytest.fixture(scope='session')
def sample_dirs():
    return testing_tools.SamplePaths(
        root='tests\\samples',
        input_='input',
        input_sprites='input\\sprites',
        input_jsons='input\\jsons',
        output='output',
    )


@pytest.fixture(scope='session', autouse=True)
def output_data(sample_dirs):
    Path(sample_dirs.output).mkdir(exist_ok=True)


@pytest.fixture
def aseprite_json():
    return {
        "frames": {
            "test_sprite_Start_0": {
                "frame": {"x": 0, "y": 32, "w": 32, "h": 32},
                "rotated": False,
                "trimmed": False,
                "spriteSourceSize": {"x": 0, "y": 0, "w": 32, "h": 32},
                "sourceSize": {"w": 32, "h": 32},
                "duration": 100
            },
            "test_sprite_Start_1": {
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
def sprite_files(sample_dirs):
    return {
        'sprites': [
            str(sample_dirs.input_sprites.joinpath('ignore_sprite.aseprite')),
            str(sample_dirs.input_sprites.joinpath('test_sprite.aseprite')),
            str(sample_dirs.input_sprites.joinpath('test_sprite2.aseprite')),
        ],
        'spritessprite_subdir': [
            str(sample_dirs.input_sprites.joinpath(
                'sprite_subdir\\test_subsprite.aseprite')),
        ]
    }


@pytest.fixture
def aseprite_cli(sprite_files, sample_dirs):
    return (
        "aseprite -b --ignore-empty --list-tags "
        f"--ignore-layer 'Reference Layer 1' "
        f"{sprite_files['sprites'][0]} "
        f"{sprite_files['sprites'][1]} "
        f"{sprite_files['sprites'][2]} "
        "--filename-format {title}_{tag}_{tagframe} "
        f"--sheet {sample_dirs.output.joinpath('sprites.png')} "
        f"--data {sample_dirs.output.joinpath('sprites.json')}"
    )
