import kivyhelper.scripts.build_assets as ba
import kivyhelper.lib as lib
from kivyhelper import constants
from tests import testing_tools


def test_assemble_aseprite_cli(sprite_files, aseprite_cli, sample_dirs):
    assert ba.assemble_aseprite_cli(
        'sprites',
        sprite_files['sprites'],
        sample_dirs.output) == aseprite_cli


def test_execute_aseprite_cli(aseprite_cli, sample_dirs):
    testing_tools.check_aseprite_skip()
    ba.execute_aseprite_cli(aseprite_cli)
    j = lib.read_aseprite_json(sample_dirs.output.joinpath('sprites.json'))
    assert list(j.keys()) == ['frames', 'meta']
    assert len(j['frames']) == 33
    assert j['meta']['size'] == dict(w=512, h=96)


def test_collect_aseprite_files(sprite_files, sample_dirs):
    assert ba.collect_files(
        sample_dirs.input_, ext=constants.ASE_EXTS) == sprite_files

    # Test ignore:
    assert ba.collect_files(
        sample_dirs.input_,
        ['ignore_', 'test_sprite[3]+'],
        ext=constants.ASE_EXTS) == {
        'sprites': sprite_files['sprites'][1:],
        'spritessprite_subdir': sprite_files['spritessprite_subdir']
    }
    assert ba.collect_files(
        sample_dirs.input_,
        ['ignore_', r'test_sprite\d+'],
        ext=constants.ASE_EXTS) == {
        'sprites': [sprite_files['sprites'][1]],
        'spritessprite_subdir': sprite_files['spritessprite_subdir']
    }

    # Test sprites in the root:
    assert ba.collect_files(
        sample_dirs.input_sprites.joinpath('sprite_subdir'),
        ext=constants.ASE_EXTS) == {
        'sprite_subdir': sprite_files['spritessprite_subdir']
    }


def test_collect_json_files(json_files, sample_dirs):
    assert ba.collect_files(
        sample_dirs.input_jsons,
        ext='.json') == json_files
