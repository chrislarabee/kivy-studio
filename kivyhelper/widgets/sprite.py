from __future__ import annotations

import re
from pathlib import Path
from random import sample
from typing import Dict, Tuple, List

from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import (ObjectProperty, StringProperty, NumericProperty)

from kivyhelper import constants


class AnimRule:
    @property
    def is_random(self) -> bool:
        return self._random

    @property
    def dependents(self) -> Dict[str, Tuple[AnimRule, ...]]:
        return self._dependents

    @dependents.setter
    def dependents(self, dependents: dict):
        def _tuple(x):
            if isinstance(x, AnimRule):
                return (x,)
            elif isinstance(x, tuple):
                return x
            else:
                raise TypeError(
                    f'Dependents must be tag: AnimRule/Tuple[AnimRule] pairs.')
        self._dependents = {k: _tuple(v) for k, v in dependents.items()}

    @property
    def parent_sprite(self) -> Sprite:
        return self._parent

    @parent_sprite.setter
    def parent_sprite(self, new_parent: Sprite):
        if isinstance(new_parent, Sprite):
            self._parent = new_parent
        else:
            raise TypeError(
                f'Anim rule parent_sprite must be a Sprite object. Passed '
                f'object type = {type(new_parent)}')

    @property
    def tags(self) -> Tuple[str, ...]:
        return self._tags

    @tags.setter
    def tags(self, anim_name: str, *tags: str):
        self._tags = self.assemble_tags(anim_name, *tags)

    @property
    def cur_tags(self) -> Tuple[str, ...]:
        return self._cur_tags

    def __init__(
            self,
            anim_name: str,
            *tag_queue: str,
            **dependents):
        """
        A one stop reference for Sprite objects to control their
        animations.

        Args:
            anim_name: The base name of the animation, to be combined
                with tags from the tag queue.
            *tag_queue: Any number of strings, the tags that can be
                found appended to each file name in an atlas created
                using KivyHelper. These will be combined with anim_name
                to form the tag queue. If at any point you want the
                AnimRule to switch to a new base anim_name, include it
                in the tag queue with a * appended to the string and it
                will be treated as a new base for the tags that follow
                it.
            **dependents: Any number of tag names and accompanying
                Sprites or iterables of Sprites that should be released
                on the tag name.
        """
        self._tags: Tuple[str, ...] = self.assemble_tags(anim_name, *tag_queue)
        self._cur_tags: Tuple[str, ...] = self.assemble_tags(
            anim_name, *tag_queue)
        self._dependents: Dict[str, Tuple[AnimRule, ...]] = dict()
        self.dependents = dependents
        self._parent: (Sprite, None) = None
        self._pos: int = 0
        self._random: bool = False
        self._z_buffer: bool = False

    @staticmethod
    def assemble_tags(anim_name: str, *tags: str) -> Tuple[str, ...]:
        result = []
        cur_root = anim_name
        for t in tags:
            if t[-1] == '*':
                cur_root = t[:-1]
            else:
                result.append(f'{cur_root}_{t}')
        return tuple(result)

    def randomize(self, z_buffer: bool = False) -> AnimRule:
        """
        Randomizes the tag queue. Intended for use with idle animations
        that have variations you want to run through in random orders.

        The first tag in the original tag queue will be treated as the
            "rest" state, and will always be the first tag in the
            randomized queue.

        Args:
            z_buffer: Set to True if you want the rest state to be
                inserted between every tag variation. So that the queue
                looks like (Rest, VariationB, Rest, VariationD...)

        Returns: self

        """
        self._random = True
        if not self._z_buffer and z_buffer:
            self._z_buffer = z_buffer
        rand_tags = sample(self.tags[1:], len(self.tags[1:]))
        z = self.tags[0]
        if self._z_buffer:
            for i in range(1, len(rand_tags) + 1, 2):
                rand_tags.insert(i, z)
        self._cur_tags = (z, *rand_tags)
        return self

    def release(self) -> None:
        """
        Activates the parent_sprite's release method.

        Returns: None

        """
        self.parent_sprite.release()

    def reset(self) -> None:
        """
        Resets the AnimRule's iteration to 0. If AnimRule has been
        randomized, will re-randomize the tag queue so that it is ready
        for another pass through it.

        Returns: None

        """
        self._pos = 0
        if self._random:
            self.randomize()

    def __next__(self) -> (str, None):
        """
        Advances the tag queue and alerts dependents if they should
        be released.

        Returns: The next animation + tag string in the tag queue, or
            None if the tag queue has been completed.

        """
        if self._pos >= len(self.cur_tags):
            return None
        else:
            t = self.cur_tags[self._pos]
            self._pos += 1
            # TODO: Figure out how to make it so that AnimRules are
            #       released upon *completion* of the tag they depend
            #       on.
            # TODO: Figure out how to make it so released AnimRule
            #       parents don't start animating the moment they are
            #       released?
            dep = self._dependents.get(t)
            if dep:
                for d in dep:
                    d.release()
            return f'{t}_'

    def __iter__(self) -> AnimRule:
        return self


class Sprite(Image):
    _atlas = ObjectProperty()
    mode = StringProperty('action')
    anim_event = ObjectProperty()
    time = NumericProperty(0.0)
    rate = NumericProperty(0.15)
    frame = NumericProperty(0)
    fps = NumericProperty(1.0 / 6.0)

    @property
    def frames(self):
        return self._frames

    @property
    def animation(self):
        return self._anim_tag

    @property
    def anim_rule(self):
        return self._anim_rule

    @anim_rule.setter
    def anim_rule(self, new_rule: AnimRule):
        self._anim_rule = self.link_rule(new_rule)

    @property
    def persist_rule(self):
        return self._persist_r

    @persist_rule.setter
    def persist_rule(self, new_rule: AnimRule):
        self._persist_r = self.link_rule(new_rule)

    def __init__(
            self,
            atlas: (str, Path),
            anim_rule: AnimRule,
            persist_rule: AnimRule = None,
            **kwargs):
        """
        Image widget designed to play animations from a spritesheet via
        a kivy Atlas.

        For Sprite's purposes, an "animation" is defined as a sequential
        grouping of frames from the spritesheet, which may be
        sub-divided into "tags." When animating, the Sprite object will
        iterate through each frame in a tag, and then, if allowed by its
        anim_rule, advance to the next tag in the animation.

        Args:
            atlas: The path to a .atlas file.
            anim_rule: An AnimRule object with information on the tag
                queue for a given animation sequence.
            persist_rule: An AnimRule object that, if provided, makes
                this Sprite persistent. Whenever it's main anim_rule is
                completed, it will return to persist_rule and use it to
                idle until it gets a new anim_rule.
            **kwargs: Keyword arguments. This is required due to
                inheriting Image widget.
        """
        super(Sprite, self).__init__(**kwargs)
        self._anim_rule: (AnimRule, None) = None
        self.anim_rule = anim_rule
        self._persist_r: (AnimRule, None) = None
        if persist_rule:
            self.persist_rule = persist_rule
        self._anim_tag: str = ''
        self._frames: Dict[str, List[str, ...]] = dict()
        self._atlas: str = ''
        self.link_atlas(atlas)

    def link_atlas(
            self,
            atlas: (str, Path),
            anim_rule: AnimRule = None) -> Sprite:
        """
        Links an atlas to this Sprite.

        Args:
            atlas: The path to a .atlas file.
            anim_rule: A new AnimRule object, if None, the existing
                AnimRule will be maintained.

        Returns: The Sprite, so that this method can be chained
            immediately into a start() method call.

        """
        self._atlas = str(atlas)
        if anim_rule:
            self.anim_rule = anim_rule
        self._anim_tag = next(self.anim_rule)
        self._frames = self.collect_frames()
        return self

    def link_rule(self, anim_rule: AnimRule) -> AnimRule:
        """
        Links the passed AnimRule to this Sprite, making the Sprite its
        parent.

        Args:
            anim_rule: An AnimRule object.

        Returns: The AnimRule object.

        """
        anim_rule.parent_sprite = self
        return anim_rule

    def collect_frames(self) -> Dict[str, List[str, ...]]:
        """
        Changes a dictionary like this:
        {"sprites_snowflake.png": {
            "white_Start_0": [0, 0, 32, 32],
            "white_Start_1": [32, 0, 32, 32],
            "white_Idle_0": [160, 0, 32, 32],
            "white_Idle_1": [192, 0, 32, 32]
            }
        }

        Into a dictionary like this:
        {"white_Start_": ["white_Start_0", "white_Start_1"],
         "white_Idle_": ["white_Idle_0", "white_Idle_1"]}

        Returns: A dictionary.

        """
        results = dict()
        for f in Atlas(self._atlas + '.atlas').textures.keys():
            m = re.match(r'(\D+)\d+', f)
            if m:
                frame = m.groups()[0]
                if frame not in results.keys():
                    results[frame] = [f]
                else:
                    results[frame].append(f)
        return results

    def update(self, dt) -> None:
        """
        Advances the sprite to the next image in the tag.

        Args:
            dt: A delta, passed by the kivy Clock.

        Returns: None

        """
        self.time += dt
        if self.time > self.rate:
            self.time -= self.rate
            f = f'{self._anim_tag}{self.frame}'
            self.source = f'atlas://{self._atlas}/{f}'
            self.frame += 1
            if self.frame >= len(self._frames[self._anim_tag]):
                self.end()

    @staticmethod
    def check_anim_tag(anim_tag: str, pat: str) -> bool:
        """
        Convenience function for checking a passed anim_tag for a passed
        pattern.
        Args:
            anim_tag: A string.
            pat: A regex pattern string.

        Returns: A boolean indicating if anim_tag matches pat.

        """
        return re.search(pat, anim_tag, flags=re.IGNORECASE) is not None

    def start(self, new: (str, AnimRule) = None) -> None:
        """
        Starts the current animation + tag's loop or the passed
        animation + tag's loop.

        Args:
            new: A string, a new animation + tag to start, or an
                AnimRule object, representing a new AnimRule to release
                into.

        Returns: None

        """
        if self.anim_event:
            self.anim_event.cancel()
        if isinstance(new, str):
            self._anim_tag = new
        elif isinstance(new, AnimRule):
            self.anim_rule = new
            self._anim_tag = next(self.anim_rule)
        idle = self.check_anim_tag(self._anim_tag, constants.IDLE)
        self.mode = 'idle' if idle else 'action'
        self.frame = 0
        self.anim_event = Clock.schedule_interval(self.update, self.fps)

    def end(self) -> None:
        """
        Restarts the tag loop if in idle mode, otherwise ends the tag
        and auto-releases to the next tag.

        Returns: None

        """
        if self.mode == 'idle':
            self.frame = 0
        else:
            self.release()

    def release(self) -> None:
        """
        Allows the Sprite to leave its current tag and advance to the
        next tag. If no tags remain and the Sprite has a persistent
        AnimRule object, returns to that state.

        Returns: None

        """
        next_anim = next(self.anim_rule)
        if next_anim:
            self.start(next_anim)
        else:
            if self.persist_rule:
                self.persist_rule.reset()
                self.anim_rule = self.persist_rule
                self.start(next(self.anim_rule))
            else:
                self.anim_event.cancel()
                self.parent.remove_widget(self)
