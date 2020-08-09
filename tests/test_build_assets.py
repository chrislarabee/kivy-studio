import kivyhelper.scripts.build_assets as ba


def test_collect_aseprite_files():
    input_ = 'tests/test_data/input'
    assert ba.collect_aseprite_files(input_) == [
        'tests\\test_data\\input\\ignore_sprite.aseprite',
        'tests\\test_data\\input\\test_sprite.aseprite',
        'tests\\test_data\\input\\test_sprite2.aseprite',
    ]
    # Test ignore:
    assert ba.collect_aseprite_files(input_, ['ignore_', 'test_sprite[3]+']) == [
        'tests\\test_data\\input\\test_sprite.aseprite',
        'tests\\test_data\\input\\test_sprite2.aseprite',
    ]
    assert ba.collect_aseprite_files(input_, ['ignore_', r'test_sprite\d+']) == [
        'tests\\test_data\\input\\test_sprite.aseprite',
    ]
