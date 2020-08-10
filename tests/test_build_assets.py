import kivyhelper.scripts.build_assets as ba


def test_collect_aseprite_files():
    input_ = 'tests/test_data/input'
    assert ba.collect_aseprite_files(input_) == {
        'sprites': [
            'tests\\test_data\\input\\sprites\\ignore_sprite.aseprite',
            'tests\\test_data\\input\\sprites\\test_sprite.aseprite',
            'tests\\test_data\\input\\sprites\\test_sprite2.aseprite',
        ],
        'spritessprite_subdir': [
            'tests\\test_data\\input\\sprites\\sprite_subdir\\test_subsprite.aseprite',
        ]
    }
    # Test ignore:
    assert ba.collect_aseprite_files(input_, ['ignore_', 'test_sprite[3]+']) == {
        'sprites': [
            'tests\\test_data\\input\\sprites\\test_sprite.aseprite',
            'tests\\test_data\\input\\sprites\\test_sprite2.aseprite',
        ],
        'spritessprite_subdir': [
            'tests\\test_data\\input\\sprites\\sprite_subdir\\test_subsprite.aseprite',
        ]
    }
    assert ba.collect_aseprite_files(input_, ['ignore_', r'test_sprite\d+']) == {
        'sprites': [
            'tests\\test_data\\input\\sprites\\test_sprite.aseprite',
        ],
        'spritessprite_subdir': [
            'tests\\test_data\\input\\sprites\\sprite_subdir\\test_subsprite.aseprite',
        ]
    }

    # Test sprites in the root:
    assert ba.collect_aseprite_files(input_ + '/sprites/sprite_subdir') == {
        'sprite_subdir': [
            'tests\\test_data\\input\\sprites\\sprite_subdir\\test_subsprite.aseprite',
        ]
    }
