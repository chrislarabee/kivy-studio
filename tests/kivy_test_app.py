import sys

from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget

import kivyhelper.widgets as wd


class SpriteVisualTest(Widget):
    ball_color = StringProperty('black')

    @property
    def widget(self):
        return self._widget

    def __init__(self, **kwargs):
        super(SpriteVisualTest, self).__init__(**kwargs)
        self._widget = BoxLayout(orientation='vertical')

        ball_rule = wd.AnimRule('black', 'Start', 'Idle')
        sp1 = wd.Sprite(
            'tests/samples/assets/sprites_snowflake',
            wd.AnimRule(
                'white', 'Start', 'Idle').set_dependents(white_Start=ball_rule)
        )
        sp2 = wd.Sprite(
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

    def swap_ball_color(self) -> wd.AnimRule:
        self.ball_color = dict(red='black', black='red')[self.ball_color]
        return wd.AnimRule(
            self.ball_color,
            'Start',
            'Idle'
        )

    def go(self):
        pass


class DialogueBoxVisualTest(Widget):
    lbl_background = ObjectProperty()

    @property
    def widget(self):
        return self._widget

    def __init__(self, **kwargs):
        super(DialogueBoxVisualTest, self).__init__(**kwargs)
        self._widget = BoxLayout(orientation='vertical')

        lines = [
            wd.DialogueLine('Alpha', 'Some test dialogue.'),
            wd.DialogueLine('Beta', 'Another line of test dialogue!'),
        ]

        lbl = wd.WrapLabel(text='Lines will appear here.')
        d = wd.DialogueBox(
            lines=lines,
            display_text_on=lbl
        )
        tt = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint=(.2, .1))

        tt.add_widget(lbl)

        with tt.canvas.before:
            Color(0, 0, 0, 1)
            self.lbl_background = Rectangle()
        tt.bind(size=lambda *x: setattr(
            self.lbl_background, 'size', x[1]))
        tt.bind(pos=lambda *x: setattr(
            self.lbl_background, 'pos', x[1]))
        a = AnchorLayout(anchor_x='center', anchor_y='center')
        a.add_widget(tt)
        d.add_widget(a)

        self._widget.add_widget(d)

        btn = Button(text='Next Line', size_hint_y=.1)
        btn.bind(on_press=lambda x: d.next_line())
        self._widget.add_widget(btn)

    def go(self):
        pass


class TooltipAnchor(AnchorLayout, wd.TooltipBehavior):
    pass


class CornerWidget(FloatLayout, wd.MouseoverBehavior):
    display_str = StringProperty('')
    tool_tip = ObjectProperty()

    def show_tool_tip(self):
        self.tool_tip = TooltipAnchor(
            size=(150, 100),
            edge_padding=10,
            anchor_x='center',
            anchor_y='center',
            size_hint=(None, None),
        )
        self.tool_tip.set_tip_pos(self.border_point)
        with self.tool_tip.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(size=self.tool_tip.size, pos=self.tool_tip.pos)
        lbl = wd.WrapLabel(
            text=f'{self.display_str}, collide={self.tool_tip.pos}'
        )
        self.tool_tip.add_widget(lbl)
        self.add_widget(self.tool_tip)

    def on_enter(self):
        self.show_tool_tip()

    def on_leave(self):
        self.remove_widget(self.tool_tip)


class MouseoverBehaviorVisualTest(Widget):
    @property
    def widget(self):
        return self._widget

    def __init__(self, **kwargs):
        super(MouseoverBehaviorVisualTest, self).__init__(**kwargs)
        self._widget = RelativeLayout()
        a = AnchorLayout(anchor_x='center', anchor_y='center')
        self._widget.add_widget(a)
        nested = RelativeLayout(size_hint=(.3, .3))
        with nested.canvas:
            Color(1, 1, 1, 1)
            r = Rectangle()
        a.add_widget(nested)
        nested.bind(size=lambda *x: setattr(r, 'size', x[1]))

        corners = [
            ['Lower left', dict(), (.8, 0, 0, 1)],
            ['Upper left', dict(top=1), (0, 0, .8, 1)],
            ['Upper right', dict(right=1, top=1), (0, .8, 0, 1)],
            ['Lower right', dict(right=1), (0, .8, .8, 1)],
        ]

        def _gen_corner(args):
            result = CornerWidget(
                display_str=args[0],
                pos_hint=args[1],
                size_hint=(.3, .3)
            )
            with result.canvas:
                Color(*args[2])
                r_ = Rectangle()
                result.bind(size=lambda *x: setattr(r_, 'size', x[1]))
                result.bind(pos=lambda *x: setattr(r_, 'pos', x[1]))
            return result

        for c in corners:
            w1 = _gen_corner(c)
            self._widget.add_widget(w1)
            w2 = _gen_corner(c)
            nested.add_widget(w2)

    def go(self):
        pass


visual_tests = dict(
    sprite=SpriteVisualTest(),
    dialogue=DialogueBoxVisualTest(),
    mouseover=MouseoverBehaviorVisualTest()
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
