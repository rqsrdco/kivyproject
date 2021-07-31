import json
import time
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from libs.uix.components.profile_preview_dialog import ProfilePreview


class SalesStaff(MDScreen):
    #menu = ListProperty(None)
    #order = ListProperty(None)
    user = StringProperty()
    times = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        Window.size = (1024, 768)
        Window.minimum_width, Window.minimum_height = Window.size
        # Window.maximize()
        Clock.schedule_interval(self.update_clock, 1)

    def update_clock(self, *args):
        self.times = time.strftime("%c")

    def open_infos(self):
        ProfilePreview().fire(title="Contact with US", image="assets/images/logoopen.png")

    def add_item_to_order(self, *args):
        if args[1]["_list_of_order"]:
            self.ids.rv_bill.data = []
            for order in args[1]["_list_of_order"]:
                bill_item = {
                    "name": order[2],
                    "quantity": order[3],
                    "price": order[4],
                    "image": args[1]["image"]
                }
                self.ids.rv_bill.add_item(bill_item)
            self.ids.rv_bill._code = args[1]["name"]
        else:
            bill_item = {
                "name": args[1]["name"],
                "quantity": args[1]["quantity"],
                "price": args[1]["price"],
                "image": args[1]["image"]
            }
            self.ids.rv_bill.add_item(bill_item)

    def show_menu(self):
        MDDialog(
            title="Options",
            type="custom",
            content_cls=MenuDialogContent()
        ).open()


class MenuDialogContent(MDBoxLayout):
    pass
