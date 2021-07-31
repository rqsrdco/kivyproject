from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior

Builder.load_string(
    """
<ListItem>
    spacing: dp(12)
    padding: dp(12)
    adaptive_height: True

    canvas.before:
        Color:
            rgba: root.bg_color
        RoundedRectangle:
            radius: [dp(12),]
            size: self.size
            pos: self.pos

    MDBoxLayout:
        adaptive_size: True
        pos_hint: {"center_y": .5}

        MDIconButton:
            icon: root.icon
            adaptive_size: True
            user_font_size: "39sp"
            theme_text_color: "Custom"
            text_color: root.icon_color if root.icon_color else app.theme_cls.primary_color

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(7)
        adaptive_height: True
        pos_hint: {"center_y": .5}

        MDLabel:
            text: root.text
            font_style: "H6"
            adaptive_height: True
            shorten: True
            shorten_from: 'right'
            text_size: self.width, None

        MDLabel:
            text: root.secondary_text
            font_style: "Button"
            text_color: 0.5, 0.5, 0.5, 0.5
            adaptive_height: True
            shorten: True
            shorten_from: 'right'
            text_size: self.width, None
    """
)


class ListItem(ButtonBehavior, ThemableBehavior, MDBoxLayout):

    bg_color = ColorProperty([0, 0, 0, 0])
    icon_color = ColorProperty([0, 0, 0, 0])

    text = StringProperty()

    secondary_text = StringProperty()

    icon = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_color = self.theme_cls.bg_normal
        self.theme_cls.bind(theme_style=self._update_bg_color)

    def _update_bg_color(self, *args):
        self.bg_color = self.theme_cls.bg_normal

    def on_state(self, instance, value):
        Animation(
            bg_color=self.theme_cls.bg_dark
            if value == "down"
            else self.theme_cls.bg_normal,
            d=0.1,
            t="in_out_cubic",
        ).start(self)
