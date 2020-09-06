import sys

from kivy.app import App
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget

import kivyhelper.widgets.sprite as sp
import kivyhelper.widgets.dialogue as di


class SpriteVisualTest(Widget):
    ball_color = StringProperty('black')

    @property
    def widget(self):
        return self._widget

    def __init__(self, **kwargs):
        super(SpriteVisualTest, self).__init__(**kwargs)
        self._widget = BoxLayout(orientation='vertical')

        ball_rule = sp.AnimRule('black', 'Start', 'Idle')
        sp1 = sp.Sprite(
            'tests/samples/assets/sprites_snowflake',
            sp.AnimRule(
                'white', 'Start', 'Idle').set_dependents(white_Start=ball_rule)
        )
        sp2 = sp.Sprite(
            'tests/samples/assets/sprites_ball',
            ball_rule
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
        start_btn.bind(on_press=lambda x: sp1.start())
        row_top.add_widget(start_btn)

        left_tray = BoxLayout()
        row_bot.add_widget(left_tray)
        right_tray = BoxLayout()
        row_bot.add_widget(right_tray)

        ball_btn = Button(text='End Ball')
        ball_btn.bind(on_press=lambda x: sp2.release())
        right_tray.add_widget(ball_btn)

        color_btn = Button(text='Swap Color')
        color_btn.bind(on_press=lambda x: sp2.start(self.swap_ball_color()))
        right_tray.add_widget(color_btn)

        self._widget.add_widget(btn_tray)

    def swap_ball_color(self) -> sp.AnimRule:
        self.ball_color = dict(red='black', black='red')[self.ball_color]
        return sp.AnimRule(
            self.ball_color,
            'Start',
            'Idle'
        )

    def go(self):
        pass


class DialogueBoxVisualTest(Widget):
    @property
    def widget(self):
        return self._widget

    def __init__(self, **kwargs):
        super(DialogueBoxVisualTest, self).__init__(**kwargs)
        self._widget = BoxLayout(orientation='vertical')

        lines = [
            di.DialogueLine('Alpha', 'Some test dialogue.'),
            di.DialogueLine('Beta', 'Another line of test dialogue!'),
        ]
        lbl = Label(text='Lines will appear here.')
        d = di.DialogueBox(
            lines,
            display_text_on=lbl
        )
        a = AnchorLayout(anchor_x='center', anchor_y='center')
        a.add_widget(lbl)
        d.add_widget(a)

        self._widget.add_widget(d)

        btn = Button(text='Next Line', size_hint_y=.1)
        btn.bind(on_press=lambda x: d.next_line())
        self._widget.add_widget(btn)

    def go(self):
        pass


visual_tests = dict(
    sprite=SpriteVisualTest(),
    dialogue=DialogueBoxVisualTest()
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
