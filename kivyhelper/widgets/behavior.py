import abc
from typing import Tuple

from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty, OptionProperty, \
    NumericProperty
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


class TooltipBehavior(Widget):
    relative_x = OptionProperty('right', options=['left', 'center', 'right'])
    relative_y = OptionProperty('above', options=['above', 'center', 'below'])
    edge_padding = NumericProperty(0.0)

    @property
    def x_mod(self):
        """
        Returns: The baseline modifier for the x position of the mouse
            cursor to determine the x position of the TooltipLayout
            relative to the mouse cursor.

        """
        if self.relative_x == 'center':
            return (self.width / 2) * -1
        elif self.relative_x == 'left':
            return self.width * -1
        else:
            return 0

    @property
    def y_mod(self):
        """
        Returns: The baseline modifier for the y position of the mouse
            cursor to determine the y position of the TooltipLayout
            relative to the mouse cursor.

        """
        if self.relative_y == 'center':
            return (self.height / 2) * -1
        elif self.relative_y == 'below':
            return self.height * -1
        else:
            return 0

    def __init__(self, **kwargs):
        """
        Mixin class to give any Widget TooltipBehavior, allowing it to
        be easily positioned relative to a mouse cursor. Designed to be
        used in tandem with a Widget that has MouseoverBehavior and
        which generates a Widget with TooltipBehavior on_enter.

        Args:
            **kwargs: Kivy kwargs. Kwargs unique to TooltipBehavior:
                relative_x: Determines where the tooltip appears
                    relative to the mouse's x position. Default is
                    'right' which places the tooltip to the right of the
                    mouse. Can also specify 'left' to place the tooltip
                    to the left, and 'center' to place the tooltip's
                    horizontal center on the mouse position.
                relative_y: Determines where the tooltip appears
                    relative to the mouse's y position. Default is
                    'above' which places the tooltip above the mouse.
                    Can  also specify 'below' to place the tooltip
                    below, and 'center' to place the tooltip's
                    vertical center on the mouse position.
                edge_padding: By default, TooltipLayout will set its
                    position such that it doesn't overflow the edges of
                    the Window. Optionally, you can specify an amount of
                    additional padding to add to prevent the edges of
                    the tooltip being flush with the edge of the
                    Window.
        """
        super(TooltipBehavior, self).__init__(**kwargs)

    def set_tip_pos(self, mouse_pos: Tuple[float, float]) -> None:
        """
        Add a call to this method in the on_enter method of the Widget
        with MouseoverBehavior that will create the TooltipLayout.

        Args:
            mouse_pos: A tuple of x and y coordinates.

        Returns: None

        """
        self.pos = self._mod_mouse_pos(*mouse_pos, Window.size)

    def _get_edge_pos(
            self,
            x: float,
            y: float) -> Tuple[float, float, float, float]:
        """
        Given an x and y coordinate, calculates where the edges of the
        TooltipLayout will be positioned relative to that coordinate,
        based on the settings of relative_x and relative_y.

        Args:
            x: An x coordinate.
            y: A y coordinate.

        Returns: A tuple containing the position of the left edge, top
            edge, right edge, and bottom edge of the TooltipLayout
            relative to the passed coordinate.

        """
        return (
            x + self.x_mod,  # Left
            y + self.height + self.y_mod,  # Top
            x + self.width + self.x_mod,  # Right
            y + self.y_mod,  # Bottom
        )

    def _mod_mouse_pos(
            self,
            x: float,
            y: float,
            window_dims: Tuple[float, float]) -> Tuple[float, float]:
        """
        Given an x and y coordinate and the dimensions of a Window,
        modifies the x and y coordinates to ensure that the
        TooltipLayout's boundaries will not be pushed outside the
        boundaries of the window dimensions.

        Args:
            x: An x coordinate.
            y: A y coordinate.
            window_dims: The width and height of the Window the app is
                running in.

        Returns: x and y, modified as necessary given their position
            relative to window_dims and the size of TooltipLayout.

        """
        left, top, right, bottom = self._get_edge_pos(x, y)
        if right >= window_dims[0]:
            x = window_dims[0] - self.width - self.edge_padding
        if left <= 0:
            x = self.edge_padding
        if top >= window_dims[1]:
            y = window_dims[1] - self.height - self.edge_padding
        if bottom <= 0:
            y = self.edge_padding
        return x, y
