from kivyhelper.handler import Handler


class TestHandler:
    def test_load_jsonlines(self, sample_dirs):
        expected = [
            dict(a=1, b=2, c=3),
            dict(a=4, b=5, c=6),
            dict(a=7, b=8, c=9),
        ]
        assert Handler._load_jsonlines(
            sample_dirs.input_jsons.joinpath('jl_sample.jsonl')
        ) == expected
