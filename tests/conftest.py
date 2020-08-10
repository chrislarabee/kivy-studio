import pytest


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