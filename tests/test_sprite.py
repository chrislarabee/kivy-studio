from random import seed

import amanuensis
import pytest

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

    def test_link_rule(self, testing_sprite):
        an = sp.AnimRule('black', 'Start', 'Idle')
        an = testing_sprite.link_rule(an)
        assert an.parent_sprite == testing_sprite


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

    def test_dependents(self, sample_dirs, testing_sprite):
        an0 = sp.AnimRule(
            'white',
            'Start',
            'Idle'
        )
        next(an0)
        testing_sprite.anim_rule = an0
        an = sp.AnimRule(
            'black',
            'Start',
            'Idle',
            black_Idle=an0
        )
        assert testing_sprite.animation == 'white_Start_'
        assert next(an) == 'black_Start_'
        assert testing_sprite.animation == 'white_Start_'
        assert next(an) == 'black_Idle_'
        assert testing_sprite.animation == 'white_Idle_'
