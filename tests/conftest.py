import warnings
from pathlib import Path

import pytest

from kivyhelper.lib import enquote
from kivyhelper.widgets.sprite import Sprite
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
        assets='assets'
    )


@pytest.fixture(scope='session', autouse=True)
def output_data(sample_dirs):
    Path(sample_dirs.output).mkdir(exist_ok=True)


@pytest.fixture
def aseprite_json():
    return {
        "frames": {
            "black_Start_0": {
                "frame": {"x": 0, "y": 32, "w": 32, "h": 32},
                "rotated": False,
                "trimmed": False,
                "spriteSourceSize": {"x": 0, "y": 0, "w": 32, "h": 32},
                "sourceSize": {"w": 32, "h": 32},
                "duration": 100
            },
            "black_Start_1": {
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
def kivy_atlas():
    return dict(
        sprites=dict(
            test_sprite_Start_0=[0, 32, 32, 32],
            test_sprite_Start_1=[32, 32, 32, 32],
        )
    )


@pytest.fixture
def sprite_files(sample_dirs):
    return {
        'sprites': [
            str(sample_dirs.input_sprites.joinpath('ignore_sprite.aseprite')),
            str(sample_dirs.input_sprites.joinpath('test_sprite2.aseprite')),
        ],
        'sprites_ball': [
            str(sample_dirs.input_sprites.joinpath(
                'ball\\black.aseprite')),
            str(sample_dirs.input_sprites.joinpath(
                'ball\\red.aseprite')),
        ],
        'sprites_snowflake': [
            str(sample_dirs.input_sprites.joinpath(
                'snowflake\\white.aseprite')),
        ]
    }


@pytest.fixture
def json_files(sample_dirs):
    return {
        'jsons': [
            str(sample_dirs.input_jsons.joinpath('aseprite_json.json')),
            str(sample_dirs.input_jsons.joinpath('std_json.json')),
        ]
    }


@pytest.fixture
def aseprite_cli(sprite_files, sample_dirs):
    return (
        'aseprite -b --ignore-empty --list-tags '
        '--ignore-layer "Reference Layer 1" '
        f'{" ".join([enquote(x) for y in sprite_files.values() for x in y])} '
        '--filename-format {title}_{tag}_{tagframe} '
        f'--sheet "{sample_dirs.output.joinpath("sprites.png")}" '
        f'--data "{sample_dirs.output.joinpath("sprites.json")}"'
    )


@pytest.fixture
def testing_sprite(sample_dirs):
    return Sprite(
        sample_dirs.assets.joinpath('sprites_snowflake'),
        'white_Idle_'
    )
