from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ColorProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout

from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivymd.uix.list import OneLineIconListItem
from kivy.graphics import Line, Color
from kivy.animation import Animation
from kivymd.color_definitions import hue, palette
#from kivymd.uix.dialog import BaseDialog
from kivymd.font_definitions import theme_font_styles
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.clock import Clock


class ColorWidget(BoxLayout):
    rgba_color = ColorProperty()


class CustomOneLineIconListItem(OneLineIconListItem):
    icon = StringProperty()


class PreviousMDIcons(Screen):
    anim_pt = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Clock.schedule_once(self._late_init)

    def on_pre_enter(self):
        Window.size = (999, 777)
        Window.minimum_width, Window.minimum_height = Window.size
        with self.canvas.before:
            Color(1, 1, 1)
            Line(points=[100, 100, 100, 200, 200, 200,
                 200, 100, 300, 100, 300, 200], width=3)

    def on_enter(self):
        self.set_list_md_icons()
        # start the red line with no points
        with self.canvas.before:
            Color(1, 0, 0)
            self.line = Line(width=5)    # saves a reference to the line

        # animate the end point (self.anim_pt)
        self.anim_pt = [100, 100]
        anim = Animation(anim_pt=[100, 200], d=3)
        anim.start(self)

    def on_anim_pt(self, widget, progress):
        # called when anim_pt changes

        # set up the line points
        points = [100, 100]
        points.extend(self.anim_pt)

        # remove the old line
        self.canvas.before.remove(self.line)

        # draw the updated line
        with self.canvas.before:
            self.line = Line(points=points, width=5)

    def set_list_md_icons(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_icon_item(name_icon):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "icon": name_icon,
                    "text": name_icon,
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        for name_icon in md_icons.keys():
            if search:
                if text in name_icon:
                    add_icon_item(name_icon)
            else:
                add_icon_item(name_icon)

    def _late_init(self, interval):
        primary_palette_items = [
            {
                "text": primary_palette,
                "divider": None,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=primary_palette: self.set_primary_palette_item(
                    x
                ),
            }
            for primary_palette in palette
        ]
        self.primary_palette_menu = MDDropdownMenu(
            caller=self.ids.primary.ids.primary_palette,
            items=primary_palette_items,
            width_mult=3,
        )

        accent_palette_items = [
            {
                "text": accent_palette,
                "divider": None,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=accent_palette: self.set_accent_palette_item(
                    x
                ),
            }
            for accent_palette in palette
        ]

        self.accent_palette_menu = MDDropdownMenu(
            caller=self.ids.accent.ids.accent_palette,
            items=accent_palette_items,
            width_mult=3,
        )

        primary_hue_items = [
            {
                "text": hue_code,
                "divider": None,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=hue_code: self.set_primary_hue_item(x),
            }
            for hue_code in hue
        ]

        self.primary_hue_menu = MDDropdownMenu(
            caller=self.ids.primary.ids.primary_hue,
            items=primary_hue_items,
            width_mult=2,
        )

        accent_hue_items = [
            {
                "text": hue_code,
                "divider": None,
                "viewclass": "OneLineListItem",
                "on_release": lambda x=hue_code: self.set_accent_hue_item(x),
            }
            for hue_code in hue
        ]

        self.accent_hue_menu = MDDropdownMenu(
            caller=self.ids.accent.ids.accent_hue,
            items=accent_hue_items,
            width_mult=2,
        )

        theme_style_items = [
            {
                "text": theme_style,
                "divider": None,
                "height": dp(54),
                "viewclass": "OneLineListItem",
                "on_release": lambda x=theme_style: self.set_theme_style_item(
                    x
                ),
            }
            for theme_style in ["Light", "Dark"]
        ]
        self.theme_style_menu = MDDropdownMenu(
            caller=self.ids.theme_style.ids.theme_style,
            items=theme_style_items,
            width_mult=3,
        )

    def set_primary_palette_item(self, text):
        self.ids.primary.ids.primary_palette.set_item(text)
        self.primary_palette_menu.dismiss()

    def set_accent_palette_item(self, text):
        self.ids.accent.ids.accent_palette.set_item(text)
        self.accent_palette_menu.dismiss()

    def set_primary_hue_item(self, text):
        self.ids.primary.ids.primary_hue.set_item(text)
        self.primary_hue_menu.dismiss()

    def set_accent_hue_item(self, text):
        self.ids.accent.ids.accent_hue.set_item(text)
        self.accent_hue_menu.dismiss()

    def set_theme_style_item(self, text):
        self.ids.theme_style.ids.theme_style.set_item(text)
        self.theme_style_menu.dismiss()
