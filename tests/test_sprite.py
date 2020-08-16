import kivyhelper.widgets.sprite as s


class TestSprite:
    def test_basics(self, sample_dirs, testing_sprite):
        assert len(testing_sprite.frames.keys()) == 2
        assert len(testing_sprite.frames['white_Start_']) == 5
        assert len(testing_sprite.frames['white_Idle_']) == 4
