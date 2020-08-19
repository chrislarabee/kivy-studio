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
            sp.AnimRule('black', 'Start', 'Idle')
        )
        b = BoxLayout()
        b.add_widget(sp1)
        b.add_widget(sp2)
        self._widget.add_widget(b)

        btn_tray = BoxLayout(size_hint_y=.2, orientation='vertical')
        row_top = BoxLayout()
        btn_tray.add_widget(row_top)
        row_bot = BoxLayout()
        btn_tray.add_widget(row_bot)

        start_btn = Button(text='Start')
        start_btn.bind(on_press=lambda x: self.start_sprite_children(b))
        row_top.add_widget(start_btn)

        left_tray = BoxLayout()
        row_bot.add_widget(left_tray)
        right_tray = BoxLayout()
        row_bot.add_widget(right_tray)

        ball_btn = Button(text='End Ball')
        ball_btn.bind(on_press=lambda x: sp2.release())
        right_tray.add_widget(ball_btn)

        color_btn = Button(text='Swap Color')
        color_btn.bind(on_press=lambda x: sp2.start(
            sp.AnimRule(
                dict(red='black', black='red')[sp2.anim_rule.anim_n],
                'Start',
                'Idle'
            )
        ))
        right_tray.add_widget(color_btn)

        self._widget.add_widget(btn_tray)

    @staticmethod
    def start_sprite_children(parent: Widget):
        for w in parent.children:
            w.start()

    def go(self):
        pass


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
