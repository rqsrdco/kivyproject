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
                            "on_press": lambda x=item, y=[]: self.add_item_to_order(x, y)
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
        # orders = self.db.get_orders_by_cashier(self.user)
        orders = self.db.get_orders()
        if orders is not None and len(orders) > 0:
            _data = []
            _out_list = [[]]
            _code = orders[0].code
            for i, item in enumerate(orders):
                if item.code != _code and i != len(orders) - 1:
                    _code = item.code
                    _out_list.append([])
                _out_list[-1].append(item)
            self._total_order = len(_out_list)
            for o in _out_list:
                _ma = o[0].code
                _money = 0
                for k in o:
                    _money += round((k.quantity * k.price), 2)
                od = {
                    "name": _ma,
                    "descriptions": str(round(_money, 2)),
                    "price": len(o),
                    "image": "assets/images/order.png",
                    "_list_of_order": o,
                    "on_press": lambda x=_ma, y=o: self.add_item_to_order(x, y)
                }
                _data.append(od)
            if self.menu_mngr.has_screen("Order"):
                self.menu_mngr.get_screen("Order").children[0].data = _data
            else:
                order_scrn = Screen()
                order_scrn.name = "Order"
                order_rv = MenuRecycleView()
                # order_rv.bind(on__selected_item=self.add_item_to_order)
                order_rv.data = _data
                order_scrn.add_widget(order_rv)
                self.menu_mngr.add_widget(order_scrn)
            if self.speed_dial.data.get("Order") is None:
                self.speed_dial.data["Order"] = "cart"
        else:
            if self.speed_dial.data.get("Order") is not None:
                self.speed_dial.data.pop("Order")
            if self.menu_mngr.has_screen("Order"):
                order = self.menu_mngr.get_screen("Order")
                self.menu_mngr.remove_widget(order)
            else:
                return

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

    def add_item_to_order(self, *args):  # json.loads(args[1])
        if args[1]:
            self.ids.rv_bill.data = []
            for order in args[1]:
                bill_item = {
                    "name": order.product,
                    "quantity": order.quantity,
                    "price": order.price,
                    "image": "assets/images/product/" + order.product + ".png"
                }
                self.ids.rv_bill.add_item(bill_item)
            self.ids.rv_bill._code = args[0]
        else:
            bill_item = {
                "name": args[0]["Product"].name,
                "quantity": 1,
                "price": args[0]["Menu"].sell_price,
                "image": "assets/images/product/" + args[0]["Product"].name + ".png"
            }
            self.ids.rv_bill.add_item(bill_item)

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
