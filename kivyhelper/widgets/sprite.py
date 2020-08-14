from pathlib import Path

from kivy.atlas import Atlas
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, StringProperty, NumericProperty


class AtlasPath:
    """
    Mimics the functionality of a pathlib.Path object, but for kivy
    atlas files.
    """
    @property
    def atlas(self):
        return self._atlas

    @property
    def png(self):
        return self._png + '/'

    @property
    def frame(self):
        return self._frame

    @property
    def dir(self):
        return self._dir + '/'

    @property
    def path(self):
        return f'{self.dir}{self.atlas}.atlas'

    def __init__(
            self,
            atlas_file: str,
            png_file: str,
            frame_base: str,
            parent_dir: str = 'assets'):
        """

        Args:
            atlas_file: The name of the atlas file.
            png_file: The name of the png file key in the atlas.
            frame_base: The frame pattern key to pull from png_file.
            parent_dir: The path to the directory atlas_file is in.
                Default is the assets folder.
        """
        p = Path(atlas_file)
        self._atlas = atlas_file if p.suffix != '.atlas' else p.stem
        self._png = png_file
        self._frame = frame_base
        self._dir = parent_dir

    def joinpath(self, f: int) -> str:
        """
        Returns the path to the frame of the passed integer.

        Args:
            f: An integer, the index of a frame that the AtlasPath
                points to.

        Returns: A string representing the path to the target frame
            index in the atlas file.

        """
        return f'atlas://{self.dir}{self.atlas}/{self.png}{self.frame}{f}'


class Sprite(Image):
    atlas_path = ObjectProperty()
    atlas = ObjectProperty()
    mode = StringProperty('action')
    anim_event = ObjectProperty()
    time = NumericProperty(0.0)
    rate = NumericProperty(0.15)
    frame_no = NumericProperty(0)
    fps = NumericProperty(1.0 / 6.0)

    def __init__(
            self,
            png: str,
            frame: str,
            atlas: str = 'sprites.atlas',
            asset_dir: str = 'assets',
            **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.atlas_path = AtlasPath(atlas, png, frame, asset_dir)
        self.atlas = Atlas(self.atlas_path.path)

    def update(self, dt):
        self.time += dt
        if self.time > self.rate:
            self.time -= self.rate
            self.source = self.atlas_path.joinpath(self.frame_no)
            self.frame_no += 1

    def loop_start(self):
        self.anim_event = Clock.schedule_interval(self.update, self.fps)


