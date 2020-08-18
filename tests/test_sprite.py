import kivyhelper.widgets.sprite as sp


class TestSprite:
    def test_basics(self, testing_sprite):
        assert len(testing_sprite.frames.keys()) == 2
        assert len(testing_sprite.frames['white_Start_']) == 5
        assert len(testing_sprite.frames['white_Idle_']) == 4
        assert testing_sprite.animation == 'white_Start_'
        assert testing_sprite.mode == 'action'
        testing_sprite.release()
        assert testing_sprite.animation == 'white_Idle_'
        assert testing_sprite.mode == 'idle'

    def test_check_anim_tag(self):
        pattern = r'(^|_)idle_'
        assert sp.Sprite.check_anim_tag('white_Idle_', pattern)
        assert not sp.Sprite.check_anim_tag('bridle', pattern)
        assert sp.Sprite.check_anim_tag('Idle_Var1', pattern)


class TestAnimRule:
    def test_basics(self):
        an = sp.AnimRule('white', 'Start', 'Idle')
        assert next(an) == 'white_Start_'
        assert next(an) == 'white_Idle_'
        assert next(an) is None

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
