import pytest

import kivyhelper.widgets.sprite as sp


class TestSprite:
    def test_basics(self, testing_sprite):
        assert len(testing_sprite.frames.keys()) == 2
        assert len(testing_sprite.frames['white_Start_']) == 5
        assert len(testing_sprite.frames['white_Idle_']) == 4


class TestAnimRule:
    def test_basics(self):
        an = sp.AnimRule('white', 'Start', 'Idle')
        assert next(an) == 'white_Start_'
        assert next(an) == 'white_Idle_'
        with pytest.raises(StopIteration):
            next(an)

    def test_dependents(self, sample_dirs, testing_sprite):
        an = sp.AnimRule(
            'black',
            'Start',
            'Idle',
            dependents=testing_sprite,
            release_on='Idle'
        )
        assert testing_sprite.animation == 'white_Start_'
        assert next(an) == 'black_Start_'
        assert testing_sprite.animation == 'white_Start_'
        assert next(an) == 'black_Idle_'
        assert testing_sprite.animation == 'white_Idle_'
