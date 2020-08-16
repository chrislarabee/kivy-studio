import re
from pathlib import Path

from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


class Sprite(Image):
    """
    Image widget designed to play an animation from a spritesheet via a
    kivy Atlas.
    """
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
        return self._animation

    def __init__(self, atlas: (str, Path), start_anim: str, **kwargs):
        """

        Args:
            atlas: The path to a .atlas file.
            start_anim: The animation from atlas to start with.
            **kwargs: Keyword arguments. This is required due to
                inheriting Image widget.
        """
        super(Sprite, self).__init__(**kwargs)
        self._sprite_mgr: SpriteManager = kwargs.get(
            'sprite_manager', SpriteManager())
        self._animation: str = ''
        self._frames: dict = dict()
        self._atlas: str = self.link_atlas(atlas, start_anim)

    def link_atlas(self, atlas: (str, Path), anim: str):
        """
        Links an atlas to this Sprite.

        Args:
            atlas: The path to a .atlas file.
            anim: The animation from atlas to start with.

        Returns:

        """
        self._atlas = str(atlas)
        self._animation = anim
        self._frames = self.collect_frames()
        return self._atlas

    def collect_frames(self):
        """

        Returns: A dictionary containing the non-enumerated frames from
        the atlas file linked to this sprite as keys, and the enumerated
        frames that fit that pattern in a list as values.

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
        Advances the sprite to the next image in the animation.

        Args:
            dt: A delta, passed by the kivy Clock.

        Returns: None

        """
        self.time += dt
        if self.time > self.rate:
            self.time -= self.rate
            f = f'{self._animation}{self.frame}'
            self.source = f'atlas://{self._atlas}/{f}'
            self.frame += 1
            if self.frame >= len(self._frames[self._animation]):
                self.loop_end()

    def loop_start(self, anim: str = None):
        """
        Starts the sprite's animation loop for the current animation or
        the passed animation.

        Args:
            anim: A string, a new animation to start.

        Returns: None

        """
        if self.anim_event:
            self.anim_event.cancel()
        if anim:
            self._animation = anim
        self.mode = 'idle' if 'idle' in self._animation.lower() else 'action'
        self.frame = 0
        self.anim_event = Clock.schedule_interval(self.update, self.fps)

    def loop_end(self):
        """
        Restarts the animation loop if in idle mode, otherwise ends the
        animation. If connected to a SpriteManager object, will tell the
        SpriteManager that its animation has ended.

        Returns:

        """
        if self.mode == 'idle':
            self.frame = 0
        else:
            if self._sprite_mgr:
                self._sprite_mgr.clear_sprite(self, self._animation)
            else:
                self.anim_event.cancel()


class SpriteManager:
    def __init__(self):
        self.sprites = dict()

    def clear_sprite(self, sprite: Sprite, anim: str):
        pass
