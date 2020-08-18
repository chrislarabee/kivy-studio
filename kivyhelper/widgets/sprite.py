import re
from pathlib import Path
from random import sample

from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import (ObjectProperty, StringProperty, NumericProperty)
import amanuensis.util as amu

from kivyhelper import constants


class AnimRule:
    @property
    def is_random(self):
        return self._random

    def __init__(
            self,
            anim_name: str,
            *tag_queue,
            dependents=None,
            release_on: str = None):
        """
        A one stop reference for Sprite objects to control their
        animations.

        Args:
            anim_name: The base name of the animation, to be combined
                with tags from the tag queue.
            *tag_queue: Any number of strings, the tags that can be
                found appended to each file name in an atlas created
                using KivyHelper.
        """
        self.anim_n: str = anim_name
        self.release_on: str = release_on
        self.tags: tuple = tag_queue
        self.cur_tags: tuple = tag_queue
        self._dependents: tuple = amu.tuplify(dependents)
        self._pos: int = 0
        self._random: bool = False
        self._z_buffer: bool = False

    def randomize(self, z_buffer: bool = False):
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
        self.cur_tags = (z, *rand_tags)
        return self

    def reset(self):
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
        Advances the tag queue and alerts dependents if the release_on
        tag has been reached.

        Returns: The next animation + tag string in the tag queue, or
            None if the tag queue has been completed.

        """
        if self._pos >= len(self.cur_tags):
            return None
        else:
            t = self.cur_tags[self._pos]
            self._pos += 1
            if self.release_on and self.release_on == t:
                for d in self._dependents:
                    d.release()
            return f'{self.anim_n}_{t}_'

    def __iter__(self):
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
        self.anim_rule: AnimRule = anim_rule
        self.persist_r: AnimRule = persist_rule
        self._anim_tag: str = ''
        self._frames: dict = dict()
        self._atlas: str = self.link_atlas(atlas)

    def link_atlas(self, atlas: (str, Path), anim_rule: AnimRule = None):
        """
        Links an atlas to this Sprite.

        Args:
            atlas: The path to a .atlas file.
            anim_rule: A new AnimRule object, if None, the existing
                AnimRule will be used.

        Returns: The Sprite, so that this method can be chained
            immediately into a start() method call.

        """
        self._atlas = str(atlas)
        self.anim_rule = anim_rule if anim_rule else self.anim_rule
        self._anim_tag = next(self.anim_rule)
        self._frames = self.collect_frames()
        return self

    def collect_frames(self) -> dict:
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

    def update(self, dt):
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

    def start(self, new: (str, AnimRule) = None):
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

    def end(self):
        """
        Restarts the tag loop if in idle mode, otherwise ends the tag
        and auto-releases to the next tag.

        Returns: None

        """
        if self.mode == 'idle':
            self.frame = 0
        else:
            self.release()

    def release(self):
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
            if self.persist_r:
                self.persist_r.reset()
                self.anim_rule = self.persist_r
                self.start(next(self.anim_rule))
            else:
                self.anim_event.cancel()
                self.parent.remove_widget(self)
