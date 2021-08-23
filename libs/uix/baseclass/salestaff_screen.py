import json
import time
from kivy.clock import Clock, mainthread
from kivy.properties import ListProperty, NumericProperty, StringProperty, ObjectProperty, DictProperty, BooleanProperty
from kivy.core.window import Window
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.toast import toast
from libs.uix.components.profile_preview_dialog import ProfilePreview
from kivy.utils import get_random_color
from kivy.graphics import Color
from kivy_garden.zbarcam import ZBarCam
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from components.menu import MenuRecycleView
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
app = MDApp.get_running_app()


class Menu(dict):
    def __init__(self, name, quantity, price, image, _list_of_order):
        dict.__init__(
            self,
            name=name,
            quantity=quantity,
            price=price,
            image=image,
            _list_of_order=_list_of_order
        )


class MenuManager(ScreenManager):
    pass


class SalesStaff(MDScreen):
    menu_mngr = ObjectProperty()
    speed_dial = ObjectProperty()
    # menu = ListProperty(None)
    # order = ListProperty(None)
    user = ObjectProperty()
    times = StringProperty()
    db = ObjectProperty()
    categories = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.db = MDApp.get_running_app().root.db
        self.categories = self.db.get_category()

        self.speed_dial = MDFloatingActionButtonSpeedDial()
        self.speed_dial.data = {}
        self.speed_dial.root_button_anim = True
        # self.speed_dial.hint_animation = True
        # self.speed_dial.bg_color_root_button = app.theme_cls.ripple_color
        # self.speed_dial.bg_color_stack_button = app.theme_cls.primary_color
        # self.speed_dial.color_icon_root_button = app.theme_cls.primary_color
        # self.speed_dial.bg_hint_color = app.theme_cls.primary_color
        # self.speed_dial.label_text_color = app.theme_cls.accent_color
        self.speed_dial.right_pad = False
        self.speed_dial.callback = self.change_menu

        self.add_widget(self.speed_dial)
        self.init_menu()

    @ mainthread
    def init_menu(self):
        if self.categories is not None and len(self.categories) > 0:
            for category in self.categories:
                screen = Screen()
                screen.name = category.name
                # MENU
                menu_rv = MenuRecycleView()
                menu_items = self.db.get_menu_by_category(category.id)
                for item in menu_items:
                    # {
                    # 'Menu': Menu(id=38, product_id=38, sell_price=29379.26),
                    # 'Product': Product(id= 38,name= Drink 37, category_id= 3),
                    # 'Category': Category(id=3, name=Drink)
                    # }
                    menu_rv.data.append(
                        {
                            "name": item["Product"].name,
                            "descriptions": item["Category"].name,
                            "price": item["Menu"].sell_price,
                            "image": "assets/images/product/" + item["Product"].name + ".png",
                            "on_press": lambda x=item: self.add_item_to_order(menu=x)
                        }
                    )

                # menu_rv.bind(on__selected_item=self.add_item_to_order)
                screen.add_widget(menu_rv)
                self.menu_mngr.add_widget(screen)

                # NAV BTN DATA
                icon = "coffee" if category.id == 1 else "food" if category.id == 2 else "cup-water"
                self.speed_dial.data["%s" % category.name] = "%s" % icon
        else:
            pass

    @ mainthread
    def show_ordered_if_exist(self, *args):
        orders = self.db.get_orders_orderBy_code()
        if orders is not None and len(orders) > 0:
            if self.speed_dial.data.get("Order") is None:
                self.speed_dial.data["Order"] = "cart"
            for order in orders:
                _data = order.pop("list_items")
                _data.append(order["name"])
                order["on_press"] = lambda x=_data: self.add_item_to_order(
                    order=x)
            if self.menu_mngr.has_screen("Order"):
                self.menu_mngr.get_screen("Order").children[0].data = orders
            else:
                order_scrn = Screen()
                order_scrn.name = "Order"
                order_rv = MenuRecycleView()
                # order_rv.bind(on__selected_item=self.add_item_to_order)
                order_rv.data = orders
                order_scrn.add_widget(order_rv)
                self.menu_mngr.add_widget(order_scrn)
        else:
            if self.speed_dial.data.get("Order") is not None:
                self.speed_dial.data.pop("Order")
            if self.menu_mngr.has_screen("Order"):
                order = self.menu_mngr.get_screen("Order")
                self.menu_mngr.remove_widget(order)
            self.speed_dial.state = "close"
            self.menu_mngr.current = "Coffee"

    def change_menu(self, instance):
        if instance.icon == "coffee":
            self.menu_mngr.current = "Coffee"
        elif instance.icon == "food":
            self.menu_mngr.current = "Food"
        elif instance.icon == "cup-water":
            self.menu_mngr.current = "Drink"
        elif instance.icon == "cart":
            self.menu_mngr.current = "Order"
        else:
            return

    def on_pre_enter(self):
        # self.init_menu()
        Clock.schedule_interval(self.update_clock, 1)

    def on_enter(self):
        Window.size = (1024, 768)
        Window.minimum_width, Window.minimum_height = Window.size
        # Window.maximize()
        Clock.schedule_once(self.show_ordered_if_exist)

    def on_pre_leave(self):
        Clock.unschedule(self.update_clock)

    def on_leave(self):
        Window.size = (636, 474)
        Window.minimum_width, Window.minimum_height = Window.size

    def show_ordered(self):
        Clock.schedule_once(self.show_ordered_if_exist)

    @ mainthread
    def update_clock(self, *args):
        self.times = time.strftime("%c")
        self.ids.lbl_bill.text_color = get_random_color(alpha=.99)

    def open_infos(self):
        ProfilePreview().fire(title="Contact with US", image="assets/images/logoopen.png")

    def add_item_to_order(self, **values):
        if 'menu' in values:
            data = values["menu"]
            order_item = {
                "name": data["Product"].name,
                "quantity": 1,
                "price": data["Menu"].sell_price,
                "image": "assets/images/product/" + data["Product"].name + ".png"
            }
            self.ids.rv_bill.add_item(order_item)
        if 'order' in values:
            datas = values["order"]
            self.ids.rv_bill.data = []
            _data = datas.copy()
            self.ids.rv_bill._code = _data.pop(-1)
            self.ids.rv_bill.data = _data
        '''
        if isinstance(values, list):
            self.ids.rv_bill.data = []
            _data = values.copy()
            self.ids.rv_bill._code = _data.pop(-1)
            self.ids.rv_bill.data = _data
            return
        if isinstance(values, dict):
            order_item = {
                "name": values["Product"].name,
                "quantity": 1,
                "price": values["Menu"].sell_price,
                "image": "assets/images/product/" + values["Product"].name + ".png"
            }
            self.ids.rv_bill.add_item(order_item)
            return'''

    def show_menu(self):
        MDDialog(
            title="Options",
            type="custom",
            content_cls=MenuDialogContent()
        ).open()

    def show_scanner(self):
        MDDialog(
            title="Scanning...",
            type="custom",
            content_cls=ScanCode()
        ).open()


class MenuDialogContent(MDBoxLayout):
    pass


class ScanCode(MDBoxLayout):
    pass
