import kivyhelper.lib as lib


def test_read_aseprite_json(aseprite_json, sample_dirs):
    assert lib.read_aseprite_json(
        sample_dirs.input_jsons.joinpath(
            'aseprite_json.json')) == aseprite_json
