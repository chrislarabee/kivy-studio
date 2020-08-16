import kivyhelper.widgets.sprite as s


class TestSprite:
    def test_basics(self, sample_dirs, testing_sprite):
        assert len(testing_sprite.frames) == 4

        sp = s.Sprite(
            sample_dirs.assets.joinpath('sprites_snowflake'),
            'white_Start_'
        )
        assert len(sp.frames) == 5
