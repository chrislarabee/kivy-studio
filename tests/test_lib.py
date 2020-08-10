import kivyhelper.lib as lib


def test_read_aseprite_json(aseprite_json):
    assert lib.read_aseprite_json(
        'tests/test_data/input/jsons/aseprite_json.json') == aseprite_json
