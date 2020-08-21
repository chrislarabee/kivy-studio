import kivyhelper.codex as cx


class SampleNode(cx.Node):
    assoc_file = 'jl_sample'

    def process(self, data: list):
        return data


class SampleCodex(cx.Codex):
    def __init__(self):
        super(SampleCodex, self).__init__()
        self.sample_data = None


class TestNode:
    def test_registry(self, sample_dirs):
        assert cx.Node.__subclasscheck__(SampleNode)


class TestCodex:
    def test_inheritance(self, sample_dirs):
        c = SampleCodex.from_dir(sample_dirs.input_jsons)
        assert isinstance(c, SampleCodex)
        assert isinstance(getattr(c, 'jl_sample'), SampleNode)
        assert isinstance(getattr(c, 'jl_sample2'), cx.DefaultNode)

    def test_from_dir(self, sample_dirs):
        c = cx.Codex.from_dir(sample_dirs.input_jsons)
        assert isinstance(getattr(c, 'jl_sample'), SampleNode)
        assert isinstance(getattr(c, 'jl_sample2'), cx.DefaultNode)

    def test_load_jsonlines(self, sample_dirs):
        expected = [
            dict(a=1, b=2, c=3),
            dict(a=4, b=5, c=6),
            dict(a=7, b=8, c=9),
        ]
        assert cx.Codex._load_jsonlines(
            sample_dirs.input_jsons.joinpath('jl_sample.jsonl')
        ) == expected

    def test_get_node_by_assoc_file(self):
        assert cx.Codex._get_node_by_assoc_file('jl_sample') == SampleNode
