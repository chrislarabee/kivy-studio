from kivy.uix.label import Label


class WrapLabel(Label):
    def __init__(self, **kwargs):
        """
        Version of kivy's Label with built in wrapping. Whatever widget
        is designated WrapLabel's parent will define the boundaries that
        any text in WrapLabel will try to fit.

        Args:
            **kwargs: Kivy kwargs.
        """
        super(WrapLabel, self).__init__(**kwargs)
        self.valign = 'top'
        self.halign = 'left'
        self.text_size = self.size[0], None
        self.height = self.texture_size[1]
