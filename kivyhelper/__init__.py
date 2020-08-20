import os
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONSOLELOG'] = '1'
from . import scripts, widgets

__all__ = ['scripts', 'widgets']
