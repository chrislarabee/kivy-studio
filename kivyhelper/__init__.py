import os
os.environ['KIVY_NO_ARGS'] = '1'

from .scripts import build_assets, new_app
from .codex import Codex, Node
from .scripts.build_assets.lib import build_assets_folder
from .scripts.new_app.lib import create_new_app
from .widgets import AnimRule, Sprite

__all__ = [
    'scripts', 'Codex', 'Node', 'Sprite', 'AnimRule', 'build_assets_folder',
    'create_new_app',
]
