import os
# kivy
from kivymd.app import MDApp
#from kivy.utils import platform
import platform
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.clock import Clock
# applibs
from core import font_definitions
from core.color_definitions import colors
from utils.configparser import config
from androspecific import statusbar
# uix
from root import Root
# kivymd
from kivymd.uix.picker import MDThemePicker


# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"


class KivyMDApp(MDApp):
    theme_icon = StringProperty("theme-light-dark")

    def __init__(self, **kwargs):
        super(KivyMDApp, self).__init__(**kwargs)
        font_definitions.register_fonts()

        self.title = "KivyMD App"
        self.icon = "assets/images/logo.png"

        self.theme_dialog = MDThemePicker()

        self.theme_cls.colors = colors
        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "Gray"
        self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = config.get_theme_style()
        self.theme_cls.font_styles.update(font_definitions.font_styles)

        Window.keyboard_anim_args = {"d": 0.2, "t": "linear"}
        Window.soft_input_mode = "below_target"

    def build(self):
        Clock.schedule_once(self.change_theme_icon)
        self.root = Root()
        self.root.set_current("authority")

    def on_start(self):
        statusbar.set_color(self.theme_cls.primary_color)

    def show_theme_picker(self):
        self.theme_dialog.open()

    def change_theme_icon(self, *args):
        self.theme_icon = (
            "moon-waxing-gibbous" if self.theme_cls.theme_style == "Light" else "white-balance-sunny"
        )

    def change_theme(self):
        def _change_theme(i):
            self.theme_cls.theme_style = (
                "Dark" if self.theme_cls.theme_style == "Light" else "Light"
            )
            config.set_theme_style(self.theme_cls.theme_style)
            self.change_theme_icon()
            print(self.theme_icon)
        Clock.schedule_once(_change_theme, .2)
