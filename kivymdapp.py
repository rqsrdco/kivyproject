import os
from datetime import date, datetime
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
    date = StringProperty()
    time = StringProperty()
    ip = StringProperty()

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
        Window.clearcolor = self.theme_cls.divider_color

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
        Clock.schedule_once(_change_theme, .2)

    def get_date(self, *args):
        '''
        Get the date to be displayed
        '''
        today = date.today()
        wd = date.weekday(today)
        days = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday', 'Sunday']
        year = str(datetime.now().year)
        month = str(datetime.now().strftime("%b"))
        day = str(datetime.now().strftime("%d"))
        date_today = f"{days[wd]}, {day} {month} {year}"
        self.date = date_today
        #now = datetime.datetime.now()
        #date = '{}/{}/{}'.format(now.month, now.day, now.year)

    def get_time(self, *agrs):
        '''
        Get the time to be displayed
        '''
        now = datetime.now()
        time = '{}:{}:{}'.format(now.hour, now.minute, now.second)
        self.time = time

    def get_ip(self, *args):
        '''
        Get the current ip.
        '''
        import socket
        self.ip = socket.gethostbyname(socket.gethostname())
