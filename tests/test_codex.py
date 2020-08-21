import kivyhelper.codex as ha


class SampleNode(ha.Node):
    assoc_file = 'jl_sample'

    def process(self, data: list):
        return data


class SampleCodex(ha.Codex):
    def __init__(self):
        super(SampleCodex, self).__init__()
        self.sample_data = None


class TestNode:
    def test_registry(self, sample_dirs):
        assert ha.Node.__subclasscheck__(SampleNode)


class TestCodex:
    def test_inheritance(self, sample_dirs):
        h = SampleCodex.from_dir(sample_dirs.input_jsons)
        assert isinstance(h, SampleCodex)
        assert getattr(h, 'jl_sample') == SampleNode
        assert getattr(h, 'jl_sample2') == ha.DefaultNode

    def test_from_dir(self, sample_dirs):
        h = ha.Codex.from_dir(sample_dirs.input_jsons)
        assert getattr(h, 'jl_sample') == SampleNode
        assert getattr(h, 'jl_sample2') == ha.DefaultNode

    def test_load_jsonlines(self, sample_dirs):
        expected = [
            dict(a=1, b=2, c=3),
            dict(a=4, b=5, c=6),
            dict(a=7, b=8, c=9),
        ]
        assert ha.Codex._load_jsonlines(
            sample_dirs.input_jsons.joinpath('jl_sample.jsonl')
        ) == expected

    def test_get_node_by_assoc_file(self):
        assert ha.Codex._get_node_by_assoc_file('jl_sample') == SampleNode
