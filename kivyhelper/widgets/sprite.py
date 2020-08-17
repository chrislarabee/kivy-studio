import re
from pathlib import Path

from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
import amanuensis.util as amu

from kivyhelper import constants


class AnimRule:
    def __init__(
            self,
            anim_name: str,
            *tag_queue,
            dependents=None,
            release_on: str = None):
        self.anim_n: str = anim_name
        self.release_on: str = release_on
        self.tags: tuple = tag_queue
        self.dependents: tuple = amu.tuplify(dependents)
        self._pos: int = 0

    def __next__(self):
        if self._pos >= len(self.tags):
            raise StopIteration
        else:
            t = self.tags[self._pos]
            self._pos += 1
            if self.release_on and self.release_on == t:
                for d in self.dependents:
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

    def __init__(self, atlas: (str, Path), anim_rule: AnimRule, **kwargs):
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
                queue and what to do when the Sprite completes a tag or
                animation.
            **kwargs: Keyword arguments. This is required due to
                inheriting Image widget.
        """
        super(Sprite, self).__init__(**kwargs)
        self.anim_rule: AnimRule = anim_rule
        self._anim_tag: str = ''
        self._frames: dict = dict()
        self._atlas: str = self.link_atlas(atlas)

    def link_atlas(self, atlas: (str, Path), anim_rule: AnimRule = None) -> str:
        """
        Links an atlas to this Sprite.

        Args:
            atlas: The path to a .atlas file.
            anim_rule: A new AnimRule object, if None, the existing
                AnimRule will be used.

        Returns: The Sprite's new atlas attribute value.

        """
        self._atlas = str(atlas)
        self.anim_rule = anim_rule if anim_rule else self.anim_rule
        self._anim_tag = next(self.anim_rule)
        self._frames = self.collect_frames()
        return self._atlas

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
                self.tag_end()

    def tag_start(self, anim_tag: str = None):
        """
        Starts the current animation + tag's loop or the passed
        animation + tag's loop.

        Args:
            anim_tag: A string, a new animation + tag to start.

        Returns: None

        """
        if self.anim_event:
            self.anim_event.cancel()
        if anim_tag:
            self._anim_tag = anim_tag
        self.mode = 'idle' if constants.IDLE in self._anim_tag.lower() else 'action'
        self.frame = 0
        self.anim_event = Clock.schedule_interval(self.update, self.fps)

    def tag_end(self):
        """
        Restarts the animation loop if in idle mode, otherwise ends the
        animation. If connected to a SpriteManager object, will tell the
        SpriteManager that its animation has ended.

        Returns:

        """
        if self.mode == 'idle':
            self.frame = 0
        else:
            try:
                self.tag_start(next(self.anim_rule))
            # TODO: Add a call to SpriteManager here.
            except StopIteration:
                self.anim_event.cancel()

    def release(self):
        """
        Allows the Sprite to leave its idle tag and advance to the next
        tag.

        Returns: None

        """
        self.tag_start(next(self.anim_rule))


class SpriteManager:
    def __init__(self):
        self.sprites = dict()
        self._sprites_list = list()

    def clear_sprite(self, sprite: Sprite, anim: str):
        pass
