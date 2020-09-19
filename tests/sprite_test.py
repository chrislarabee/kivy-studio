from random import seed

import pytest

import kivyhelper.widgets.sprite as sp


class TestSprite:
    def test_basics(self, testing_sprite):
        assert len(testing_sprite.frames.keys()) == 2
        assert len(testing_sprite.frames['white_Start_']) == 5
        assert len(testing_sprite.frames['white_Idle_']) == 4
        assert testing_sprite.animation == ''
        assert testing_sprite.mode == 'continue'
        testing_sprite.start()
        assert testing_sprite.animation == 'white_Start_'
        assert testing_sprite.mode == 'continue'

    def test_check_anim_tag(self):
        pattern = r'(^|_)idle_'
        assert sp.Sprite.check_anim_tag('white_Idle_', pattern)
        assert not sp.Sprite.check_anim_tag('bridle', pattern)
        assert sp.Sprite.check_anim_tag('Idle_Var1', pattern)

    def test_link_rule(self, testing_sprite):
        an = sp.AnimRule('black', 'Start', 'Idle')
        an = testing_sprite.link_rule(an)
        assert an.parent_sprite == testing_sprite

    def test_start(self, testing_sprite):
        t = testing_sprite.start()
        assert t == 0.83

    def test_get_anim_time(self, testing_sprite):
        assert testing_sprite.get_anim_time('white_Start_') == 0.83
        assert testing_sprite.get_anim_time('white_Idle_') == 0.67

    def test_get_total_anim_time(self, testing_sprite):
        assert testing_sprite.get_total_anim_time() == 1.5


class TestAnimRule:
    def test_basics(self, testing_sprite):
        an = sp.AnimRule('white', 'Start', 'Idle')
        assert next(an) == 'white_Start_'
        assert next(an) == 'white_Idle_'
        assert next(an) is None

        with pytest.raises(
                TypeError, match='Dependents must be tag: AnimRule'):
            an.dependents = {'Idle': 'test'}

        an.parent_sprite = testing_sprite
        assert an.parent_sprite == testing_sprite
        with pytest.raises(
                TypeError,
                match="Sprite object. Passed object type = <class 'str'>"):
            an.parent_sprite = 'bad_parent'

    def test_assemble_tags(self):
        expected = ('white_Start', 'white_Idle', 'black_Start', 'black_Idle')
        assert sp.AnimRule.assemble_tags(
            'white', 'Start', 'Idle', 'black*', 'Start', 'Idle') == expected

    def test_randomize(self):
        seed(5)
        tag_queue = ('Base', 'VarA', 'VarB', 'VarC')
        an = sp.AnimRule('Idle', *tag_queue)
        assert not an.is_random
        assert an.randomize() == an
        assert an.is_random
        expected = ('Idle_Base', 'Idle_VarA', 'Idle_VarB', 'Idle_VarC')
        assert an.tags == expected
        assert an.cur_tags == (
            'Idle_Base', 'Idle_VarC', 'Idle_VarB', 'Idle_VarA')
        an.randomize(True)
        assert an.tags == expected
        assert an.cur_tags == (
            'Idle_Base', 'Idle_VarC', 'Idle_Base', 'Idle_VarA', 'Idle_Base',
            'Idle_VarB')
        an.reset()
        assert an.tags == expected
        assert an.cur_tags == (
            'Idle_Base', 'Idle_VarA', 'Idle_Base', 'Idle_VarC', 'Idle_Base',
            'Idle_VarB')

    def test_set_dependents(self):
        an0 = sp.AnimRule('black', 'Start', 'Idle')
        an = sp.AnimRule('white', 'Start', 'Idle').set_dependents(
            white_Start=an0)
        assert an.dependents == dict(white_Start=(an0,))

    def test_set_atlas_change(self, sample_dirs, testing_sprite):
        an = sp.AnimRule('Idle', 'Base', 'VarA').set_atlas_change(
            Idle_Base=sample_dirs.assets.joinpath('sprites_ball'))
        assert an.atlas_change == dict(
            Idle_Base=sample_dirs.assets.joinpath('sprites_ball'))

        testing_sprite.anim_rule = an
        assert next(an) == 'Idle_Base_'
        assert testing_sprite._atlas == (
            'tests\\samples\\assets\\sprites_snowflake')
        assert next(an) == 'Idle_VarA_'
        assert testing_sprite._atlas == (
            'tests\\samples\\assets\\sprites_ball')
