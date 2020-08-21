import kivyhelper.handler as ha


class SampleNode(ha.Node):
    assoc_file = 'jl_sample'

    def process(self, data: list):
        return data


class TestNode:
    def test_registry(self, sample_dirs):
        assert ha.Node.__subclasscheck__(SampleNode)


class TestHandler:
    def test_from_dir(self, sample_dirs):
        h = ha.Handler.from_dir(sample_dirs.input_jsons)
        assert getattr(h, 'jl_sample') == SampleNode
        assert getattr(h, 'jl_sample2') == ha.DefaultNode

    def test_load_jsonlines(self, sample_dirs):
        expected = [
            dict(a=1, b=2, c=3),
            dict(a=4, b=5, c=6),
            dict(a=7, b=8, c=9),
        ]
        assert ha.Handler._load_jsonlines(
            sample_dirs.input_jsons.joinpath('jl_sample.jsonl')
        ) == expected

    def test_get_node_by_assoc_file(self):
        assert ha.Handler.get_node_by_assoc_file('jl_sample') == SampleNode
