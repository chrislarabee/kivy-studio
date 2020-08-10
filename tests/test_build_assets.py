import kivyhelper.scripts.build_assets as ba

from tests import testing_tools


def test_assemble_aseprite_cli(sprite_files, aseprite_cli):
    assert ba.assemble_aseprite_cli(
        'sprites', sprite_files['sprites'], 'tests/test_data/output') == aseprite_cli


def test_execute_aseprite_cli(aseprite_cli):
    testing_tools.check_aseprite_skip()
    ba.execute_aseprite_cli(aseprite_cli)


def test_collect_aseprite_files(sprite_files):
    input_ = 'tests/test_data/input'
    assert ba.collect_aseprite_files(input_) == sprite_files

    # Test ignore:
    assert ba.collect_aseprite_files(input_, ['ignore_', 'test_sprite[3]+']) == {
        'sprites': sprite_files['sprites'][1:],
        'spritessprite_subdir': sprite_files['spritessprite_subdir']
    }
    assert ba.collect_aseprite_files(input_, ['ignore_', r'test_sprite\d+']) == {
        'sprites': [sprite_files['sprites'][1]],
        'spritessprite_subdir': sprite_files['spritessprite_subdir']
    }

    # Test sprites in the root:
    assert ba.collect_aseprite_files(input_ + '/sprites/sprite_subdir') == {
        'sprite_subdir': sprite_files['spritessprite_subdir']
    }
