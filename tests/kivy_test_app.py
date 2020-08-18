import sys

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

import kivyhelper.widgets.sprite as sp


class SpriteVisualTest(Widget):
    @property
    def widget(self):
        return self._widget

    def __init__(self, **kwargs):
        super(SpriteVisualTest, self).__init__(**kwargs)
        self._widget = BoxLayout(orientation='vertical')

        sp1 = sp.Sprite(
            'tests/samples/assets/sprites_snowflake',
            sp.AnimRule('white', 'Start', 'Idle')
        )
        sp2 = sp.Sprite(
            'tests/samples/assets/sprites_ball',
            sp.AnimRule('black', 'Idle')
        )
        b = BoxLayout()
        b.add_widget(sp1)
        b.add_widget(sp2)
        self._widget.add_widget(b)
        btn = Button(size_hint_y=.1, text='End Ball')
        self._widget.add_widget(btn)
        btn.bind(on_press=lambda x: sp2.release())

    def go(self):
        for w in self._widget.children[1].children:
            print(w.animation)
            w.start()


visual_tests = dict(
    sprite=SpriteVisualTest(),
)


class KivyTestApp(App):
    b_ground = ObjectProperty()

    def __init__(self, **kwargs):
        super(KivyTestApp, self).__init__(**kwargs)
        self.visual_test = visual_tests[sys.argv[1]]

    def build(self):
        a = AnchorLayout(anchor_x='center', anchor_y='center')
        a.add_widget(self.visual_test.widget)
        a.bind(size=self.update_b_ground)
        with a.canvas.before:
            Color(1, 1, 1, .5)
            self.b_ground = Rectangle()

        return a

    def on_start(self):
        self.visual_test.go()

    def update_b_ground(self, *args):
        self.b_ground.size = args[1]


if __name__ == '__main__':
    KivyTestApp().run()
