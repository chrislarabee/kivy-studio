import kivyhelper.scripts.build_assets as ba


def test_assemble_aseprite_cli(sprite_files):
    expected = (
        "aseprite -b --ignore-empty --list-tags "
        f"{sprite_files['sprites'][0]} "
        f"{sprite_files['sprites'][1]} "
        f"{sprite_files['sprites'][2]} "
        "--sheet tests/test_data/output/sprites.png "
        "--data tests/test_data/output/sprites.json"
    )
    assert ba.assemble_aseprite_cli(
        'sprites', sprite_files['sprites'], 'tests/test_data/output') == expected


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
