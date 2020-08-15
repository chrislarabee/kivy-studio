from pathlib import Path

import kivyhelper.scripts.build_assets as ba
import kivyhelper.lib as lib
from kivyhelper import constants
from tests import testing_tools


def test_build_assets_folder(sample_dirs, sprite_files):
    asset_path = Path(sample_dirs.output, 'assets')
    if asset_path.exists():
        testing_tools.drop_test_dir(asset_path)
    atlas = ba.build_assets_folder(
        sample_dirs.input_,
        sample_dirs.output,
        ['ignore_', 'test_sprite']
    )
    for k, v in atlas.items():
        assert Path(sample_dirs.output, 'assets', k + '.atlas').exists()


def test_execute_aseprite_cli(aseprite_cli, sample_dirs):
    testing_tools.check_aseprite_skip()
    print(aseprite_cli)
    ba.execute_cli_str(aseprite_cli)
    j = lib.read_aseprite_json(sample_dirs.output.joinpath('sprites.json'))
    assert list(j.keys()) == ['frames', 'meta']
    assert len(j['frames']) == 58
    assert j['meta']['size'] == dict(w=512, h=160)


def test_assemble_aseprite_cli(sprite_files, aseprite_cli, sample_dirs):
    assert ba.assemble_aseprite_cli(
        'sprites',
        [x for y in sprite_files.values() for x in y],
        sample_dirs.output) == aseprite_cli


def test_collect_aseprite_files(sprite_files, sample_dirs):
    assert ba.collect_files(
        sample_dirs.input_, ext=constants.ASE_EXTS) == sprite_files

    # Test ignore:
    assert ba.collect_files(
        sample_dirs.input_,
        ['ignore_', 'test_sprite[3]+'],
        ext=constants.ASE_EXTS) == {
        'sprites': sprite_files['sprites'][1:],
        'sprites_ball': sprite_files['sprites_ball'],
        'sprites_snowflake': sprite_files['sprites_snowflake'],
    }
    assert ba.collect_files(
        sample_dirs.input_,
        ['ignore_', r'test_sprite\d+'],
        ext=constants.ASE_EXTS) == {
        'sprites_ball': sprite_files['sprites_ball'],
        'sprites_snowflake': sprite_files['sprites_snowflake'],
    }

    # Test sprites in the root:
    assert ba.collect_files(
        sample_dirs.input_sprites.joinpath('ball'),
        ext=constants.ASE_EXTS) == {
        'ball': sprite_files['sprites_ball']
    }


def test_collect_json_files(json_files, sample_dirs):
    assert ba.collect_files(
        sample_dirs.input_jsons,
        ext='.json') == json_files


def test_convert_ase_json_to_atlas(aseprite_json):
    expected = {
        'sprites.png': dict(
            black_Start_0=[0, 32, 32, 32],
            black_Start_1=[32, 32, 32, 32],
        )
    }
    assert ba.convert_ase_json_to_atlas(aseprite_json) == expected
