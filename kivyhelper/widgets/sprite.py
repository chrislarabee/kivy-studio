import re
from pathlib import Path

from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


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
        return self._animation

    def __init__(
            self,
            atlas: (str, Path),
            start_anim: str,
            **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self._animation = start_anim
        self._atlas = str(atlas)
        self._sprite_mgr = kwargs.get('sprite_manager', SpriteManager())
        self._frames = []
        self.collect_frames()

    def link_atlas(self, atlas: (Atlas, str, Path), anim: str):
        self._atlas = atlas if isinstance(atlas, Atlas) else Atlas(str(atlas))
        self._animation = anim
        self.collect_frames()
        return self._atlas

    def collect_frames(self):
        self._frames = []
        for f in Atlas(self._atlas + '.atlas').textures.keys():
            if re.match(re.compile(self._animation + r'\d+'), f):
                self._frames.append(f)

    def animate(self):
        self.anim_event = Clock.schedule_interval(self.update, self.fps)

    def update(self, dt):
        self.time += dt
        if self.time > self.rate:
            self.time -= self.rate
            f = f'{self._animation}{self.frame}'
            self.source = f'atlas://{self._atlas}/{f}'
            self.frame += 1
            if self.frame >= len(self._frames):
                self.loop_end()

    def loop_start(self, anim: str = None):
        if self.anim_event:
            self.anim_event.cancel()
        if anim:
            self._animation = anim
        if 'idle' in self._animation.lower():
            self.mode = 'idle'
        self.frame = 0
        self.collect_frames()
        self.animate()

    def loop_end(self):
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
