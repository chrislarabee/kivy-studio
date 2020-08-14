import kivyhelper.widgets.sprite as s


class TestAtlasPath:
    def test_basics(self):
        a = s.AtlasPath('test', 'sprites.png', 'test_sprite_Start_')
        assert a.joinpath(0) == (
            'atlas://assets/test/sprites.png/test_sprite_Start_0'
        )
        a = s.AtlasPath('test.atlas', 'sprites.png', 'test_sprite_Start_')
        assert a.joinpath(0) == (
            'atlas://assets/test/sprites.png/test_sprite_Start_0'
        )


class TestSprite:
    def test_basics(self):
        sp = s.Sprite(
            'sprites.png',
            'test_sprite_Start_',
            asset_dir='tests/samples/assets'
        )
        assert len(sp.atlas.textures.keys()) == 16
