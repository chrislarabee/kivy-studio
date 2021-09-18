from __future__ import annotations

from functools import partial
from typing import List

from kivy.clock import Clock
from kivy.properties import (NumericProperty, ObjectProperty, BooleanProperty)
from kivy.uix.floatlayout import FloatLayout


class DialogueLine:
    def __init__(self, speaker: str, text: str):
        """
        Simple object expected by DialogueBox. Use this as the parent
        object for any custom DialogueLine-like objects you create to
        ensure they work with DialogueBox.

        Args:
            speaker: The name of a line's speaker.
            text: The text of a line.
        """
        self.speaker = speaker
        self.text = text


DialogueLines = List[DialogueLine]


class DialogueBox(FloatLayout):
    display_text_on = ObjectProperty()
    display_spkr_on = ObjectProperty()
    speed = NumericProperty(0.01)
    complete = BooleanProperty(False)

    def __init__(self, **kwargs):
        """
        Widget designed to display dialogue character by character, and
        the name of the speaker of said dialogue.

        Args:
            **kwargs: Keyword arguments.
                lines: A set of lines of dialogue, converted into
                    DialogueLines objects.
        """
        if 'lines' in kwargs.keys():
            lines = kwargs.pop('lines')
        else:
            lines = []
        super(DialogueBox, self).__init__(**kwargs)
        self.lines: DialogueLines = lines
        self._pos: int = 0
        self._frame: float = 0
        self._events: list = []

    def next_line(self, dt=None) -> (float, None):
        """
        Schedules a series of Clock events, one for each character to
        display in the next line of dialogue.

        Args:
            dt: Elapsed time between scheduling this call and actual
                call, passed by the kivy Clock.

        Returns: The time it will take to display the line from start to
            finish.

        """
        if not self.complete:
            d_line = self.lines[self._pos]
            self.reset_dialogue()
            if self.display_spkr_on:
                self.display_spkr_on.text = d_line.speaker
            t = self.get_text_time(self._pos)
            for char in d_line.text:
                self._events.append(Clock.schedule_once(
                    partial(self.next_char, char), self._frame
                ))
                self._frame += self.speed
            self._pos += 1
            if self._pos >= len(self.lines):
                self.complete = True
            return t

    def get_text_time(self, line_idx: int) -> float:
        """

        Args:
            line_idx: The index of a line in the DialogueLines attached
                to this DialogueBox.

        Returns: The time in seconds it will take to complete that line
            from start to finish.

        """
        return round(len(self.lines[line_idx].text), 2)

    def get_total_text_time(self) -> float:
        """

        Returns: The total time it will take to run through every line
            of dialogue found in the DialogueLines attached to this
            DialogueBox.

        """
        total = 0
        for i in range(len(self.lines)):
            total += self.get_text_time(i)
        return total

    def next_char(self, char: str, dt):
        """
        Adds the passed character to the widget linked to the
        display_text_on property on this DialogueBox.

        Args:
            char: The character to add.
            dt: A time delta, passed by the kivy Clock.

        Returns:

        """
        self.display_text_on.text += char

    def reset_dialogue(self) -> None:
        """
        Resets the display of dialogue to blank values and prepares the
        DialogueBox to display the next line.

        Returns: None

        """
        self._frame = 0
        self.display_text_on.text = ''
        if self.display_spkr_on:
            self.display_spkr_on.text = ''
        if len(self._events) > 0:
            for event in self._events:
                event.cancel()
            self._events = []

    def reset(self) -> None:
        """
        Resets the DialogueBox entirely to its starting state.

        Returns: None

        """
        self._pos = 0
        self.complete = False
        self.reset_dialogue()

    def link_lines(self, new_lines: DialogueLine) -> DialogueBox:
        """
        Convenience method for changing the lines attached to this
        DialogueBox and resetting it at the same time.

        Args:
            new_lines: A new list of DialogueLine objects.

        Returns: self

        """
        self.lines = new_lines
        self.reset()
        return self
