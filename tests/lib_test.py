import kivyhelper.lib as lib


def test_enquote():
    assert lib.enquote('abc') == '"abc"'
    assert f"{lib.enquote('abc')}" == '"abc"'
    assert f"{' '.join([lib.enquote(x) for x in ['a 1', 'b 2', 'c 2']])}" == (
        '"a 1" "b 2" "c 2"'
    )


def test_read_aseprite_json(aseprite_json, sample_dirs):
    assert lib.read_aseprite_json(
        sample_dirs.input_jsons.joinpath(
            'aseprite_json.json')) == aseprite_json
