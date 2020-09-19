import abc

from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget


class MouseoverBehavior(Widget):
    hovered = BooleanProperty(False)
    border_point = ObjectProperty()

    def __init__(self, **kwargs):
        """
        Mixin class to give any Widget MouseoverBehavior, causing an
        event to trigger when the mouse enters or exits the boundaries
        of the Widget.

        Args:
            **kwargs: Kivy kwargs.
        """
        super(MouseoverBehavior, self).__init__(**kwargs)
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args) -> None:
        """
        Dispatches on_enter and on_leave methods when the mouse enters
        the boundaries of the widget with MouseoverBehavior.

        Args:
            *args: Pos args passed by kivy, the second one is the
                collide point, which is all that matters for this
                method.

        Returns: None

        """
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*pos)
        if self.hovered == inside:
            return
        self.border_point = pos
        self.hovered = inside
        if inside:
            self.dispatch('on_enter')
        else:
            self.dispatch('on_leave')

    @abc.abstractmethod
    def on_enter(self):
        pass

    @abc.abstractmethod
    def on_leave(self):
        pass
