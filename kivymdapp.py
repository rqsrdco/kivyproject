import os
import sys
from datetime import date, datetime
# kivy
from kivy.utils import platform
#import platform
from kivy.properties import StringProperty, ObjectProperty
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
from kivymd.uix.dialog import MDDialog
from kivymd.app import MDApp
# db
from sqlalchemy_sqlite import AlchemySQLite
# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform == "win":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.INTERNET,
    ])


class KivyMDApp(MDApp):
    db = ObjectProperty()
    theme_icon = StringProperty("theme-light-dark")
    date = StringProperty()
    time = StringProperty()
    ip = StringProperty()

    def __init__(self, **kwargs):
        print(f"\nApp------------__init__({kwargs})")
        self.db = AlchemySQLite()
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
        Window.clearcolor = (1, 1, 1, 0)

    def build(self):
        print("\nApp------------build()")
        Clock.schedule_once(self.change_theme_icon)
        self.root = Root()
        self.root.set_current("authority")

    def on_start(self):
        print("\nApp------------on_start()")
        statusbar.set_color(self.theme_cls.primary_color)

    def show_theme_picker(self):
        self.theme_dialog.open()

    def change_theme_icon(self, *args):
        self.theme_icon = (
            "moon-waxing-gibbous" if self.theme_cls.theme_style == "Light" else "white-balance-sunny"
        )

    def change_theme(self):
        '''
        CHange theme Light / Dark
        '''
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
        #clock_time = datetime.strftime(datetime.now(), "%I:%M:%S %p")

    def get_local_IP(self):
        import socket
        try:
            host_name = socket.gethostname()
            local_ip = socket.gethostbyname(host_name)
            print("Local IP: ", local_ip)
        except Exception:
            MDDialog(
                text="Unable to get Local IP",
                radius=[20, 7, 20, 7],
            ).open()

    def get_public_IP(self):
        import requests
        try:
            public_ip = requests.get(
                'http://www.icanhazip.com').content.decode()
            print("Public IP: ", public_ip)
        except Exception:
            MDDialog(
                text="Unable to get Public IP",
                radius=[20, 7, 20, 7],
            ).open()
