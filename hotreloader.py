"""
HotReloader
-----------
Uses kaki module for Hot Reload (limited to some uses cases).
Before using, install kaki by `pip install kaki`

"""


import os
import platform
import sys

root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_dir, "libs", "applibs"))
sys.path.insert(0, os.path.join(root_dir, "libs", "uix"))
sys.path.insert(0, os.path.join(root_dir, "local_database"))

from kaki.app import App as HotReloaderApp  # NOQA: E402
from kivy.logger import LOG_LEVELS, Logger  # NOQA: E402

Logger.setLevel(LOG_LEVELS["debug"])

from kivy.core.window import Window  # NOQA: E402
from kivymd.app import MDApp  # NOQA: E402

from libs.uix.root import Root  # NOQA: E402

# This is needed for supporting Windows 10 with OpenGL < v2.0
if platform.system() == "Windows":
    os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"

KV_FOLDER = os.path.join(os.getcwd(), "libs", "uix", "kv")


class KivyMDApp(MDApp, HotReloaderApp):  # NOQA: N801
    DEBUG = 1  # To enable Hot Reload

    # *.kv files to watch
    KV_FILES = [os.path.join(KV_FOLDER, i) for i in os.listdir(KV_FOLDER)]

    # Class to watch from *.py files
    # You need to register the *.py files in libs/uix/baseclass/*.py
    CLASSES = {
        "Root": "libs.uix.root",
        "AuthorityScreen": "libs.uix.baseclass.authority_screen",
        "AdminScreen": "libs.uix.baseclass.admin_screen",
        "PreviousMDIcons": "libs.uix.baseclass.mdicons_screen",
        "SalesStaff": "libs.uix.baseclass.salestaff_screen",
        "MenuRecycleView": "libs.uix.components.menu",
        "BillRecycleView": "libs.uix.components.bill",
        "ListItem": "libs.uix.components.listitem",
        "Button_Item": "libs.uix.components.bottomnav",
        "ProfilePreview": "libs.uix.components.profile_preview_dialog"
    }  # NOQA: F821

    # Auto Reloader Path
    AUTORELOADER_PATHS = [
        (".", {"recursive": True}),
    ]

    def __init__(self, **kwargs):
        super(KivyMDApp, self).__init__(**kwargs)
        Window.soft_input_mode = "below_target"
        self.title = "Python Kivy"

        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.primary_hue = "500"

        self.theme_cls.accent_palette = "Gray"
        self.theme_cls.accent_hue = "500"

        self.theme_cls.theme_style = "Dark"

    def build_app(self):  # build_app works like build method
        abc = Root()
        abc.set_current('authority')
        return abc


if __name__ == "__main__":
    KivyMDApp().run()
