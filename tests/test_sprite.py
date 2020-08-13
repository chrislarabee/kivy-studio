import kivyhelper.widgets.sprite as s


class TestAtlasPath:
    def test_basics(self):
        a = s.AtlasPath('test', 'sprites.png', 'test_sprite_Start_')
        assert a.joinpath(0) == (
            'atlas://assets/test/sprites.png/test_sprite_Start_0'
        )
