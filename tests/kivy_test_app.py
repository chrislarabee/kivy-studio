import sys

from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import Widget

from kivyhelper.widgets.sprite import Sprite


class SpriteVisualTest(Widget):
    @property
    def widget(self):
        return self._widget

    def __init__(self, **kwargs):
        super(SpriteVisualTest, self).__init__(**kwargs)
        self._widget = Sprite(
            'tests/samples/assets/sprites_snowflake',
            'white_Idle_'
        )

    def go(self):
        self._widget.loop_start()


visual_tests = dict(
    sprite=SpriteVisualTest(),
)


class KivyTestApp(App):
    def __init__(self, **kwargs):
        super(KivyTestApp, self).__init__(**kwargs)
        self.visual_test = visual_tests[sys.argv[1]]

    def build(self):
        a = AnchorLayout(anchor_x='center', anchor_y='center')
        a.add_widget(self.visual_test.widget)
        return a

    def on_start(self):
        self.visual_test.go()


if __name__ == '__main__':
    KivyTestApp().run()
