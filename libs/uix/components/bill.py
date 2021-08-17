from kivy.properties import ColorProperty, StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.theming import ThemableBehavior
from kivy.uix.recycleview import RecycleView
from kivymd.uix.card import MDCard
import time
from datetime import date, datetime
from kivymd.app import MDApp
from kivymd.toast import toast
from kivy.clock import mainthread
import model

Builder.load_string(
    """
<BillListItem>
    padding: [dp(6), dp(6), dp(6), dp(6)]
    size_hint_y: None
    height: dp(68)
    orientation: "horizontal"
    elevation: 18
    focus_behavior: True
    ripple_behavior: True
    focus_color: app.theme_cls.ripple_color
    unfocus_color: app.theme_cls.divider_color
    md_bg_color: app.theme_cls.divider_color
    radius: [12]

    MDBoxLayout:
        adaptive_size: True
        pos_hint: {"center_y": .5}

        FitImage:
            source: root.image
            size_hint: None, None
            size: dp(52), dp(52)
            radius: [dp(18),]

    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(7)
        padding: [0, dp(6), 0, dp(6)]
        adaptive_width: True
        pos_hint: {"center_y": .5}

        MDLabel:
            text: root.name
            adaptive_height: True
            halign: "center"
            font_style: "Body2"
            text_color: app.theme_cls.text_color
            text_size: self.width, None

        MDLabel:
            text: str(root.quantity)
            halign: "center"
            font_style: "Button"
            text_color: app.theme_cls.text_color
            text_size: self.width, None
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(7)
        padding: [0, dp(6), 0, dp(6)]
        adaptive_width: True
        pos_hint: {"center_y": .5}

        MDLabel:
            text: "Price"
            halign: "center"
            font_style: "Subtitle2"
            text_color: app.theme_cls.text_color
            adaptive_width: True
            text_size: self.width, None

        MDLabel:
            text: "{:,.2f} vnd".format(root.price)
            halign: "center"
            text_color: app.theme_cls.text_color
            adaptive_width: True
            text_size: self.width, None
            font_style: "Button"

    MDBoxLayout:
        orientation: 'horizontal'
        spacing: dp(7)
        adaptive_width: True
        MDIconButton:
            #adaptive_height: True
            icon: "minus"
            #user_font_size: "18sp"
            theme_text_color: "Custom"
            text_color: app.theme_cls.accent_color
            pos_hint: {'center_y': .5}
            on_release: root._minus_amount()
            size_hint: None, None
            size: dp(39),dp(39),
        MDIconButton:
            #adaptive_width: True
            icon: "plus"
            #user_font_size: "18"
            theme_text_color: "Custom"
            text_color: [0,1,0,.95]
            pos_hint: {'center_y': .5}
            on_release: root._plus_amount()
            size_hint: None, None
            size: dp(39),dp(39),
        MDIconButton:
            adaptive_height: True
            icon: "delete"
            #user_font_size: "18"
            theme_text_color: "Custom"
            text_color: [1,0,0,.95]
            pos_hint: {'center_y': .5}
            on_release: root._delete_item()
            size_hint: None, None
            size: dp(39),dp(39),

<BillRecycleView>
    canvas.before:
        Color:
            rgba: app.theme_cls.divider_color if self.data else app.theme_cls.accent_color
        RoundedRectangle:
            radius: [12]
            size: self.size
            pos: self.pos
    viewclass: 'BillListItem'
    bar_width: dp(0)
    RecycleBoxLayout:
        #padding: dp(6)
        spacing: dp(9)
        orientation: "vertical"
        size_hint_y: None
        height: self.minimum_size[1]
        default_size_hint: 1, None
        default_size: None, None
        #color:app.theme_cls.primary_color
    """
)


class BillRecycleView(RecycleView):
    _code = StringProperty(None)
    _total_price = NumericProperty(0)
    _sub_total = NumericProperty(0)
    _quantity = NumericProperty(0)
    _tax = NumericProperty(.05)
    db = ObjectProperty()

    def __init__(self, **kwargs):
        super(BillRecycleView, self).__init__(**kwargs)
        self.data = []
        self.db = MDApp.get_running_app().root.db

    def _update(self):
        if not self.data:
            self._code = ""
            self._sub_total = 0
            self._quantity = 0
            self._total_price = 0
        else:
            self._sub_total = 0
            self._quantity = len(self.data)
            self._total_price = 0
            for item in self.data:
                self._sub_total += round(item["quantity"] * item["price"], 2)
            self._total_price = round(
                ((self._sub_total * self._tax) + self._sub_total), 2)
        self.refresh_from_data()

    def on_data(self, *args):
        self._update()

    def generate_curr_bill_code(self):
        cs_u = MDApp.get_running_app().root.get_screen("salesstaff").user.email
        self._code = "%s_%s_%s" % (cs_u, self._quantity, self._total_price)

    def _insert_to_bills(self):
        bills = []
        for order in self.data:
            _cur_bill = model.Bill(
                code=self._code,
                quantity=order["quantity"],
                price=order["price"],
                product=order["name"],
                cashier_id=MDApp.get_running_app().root.get_screen('salesstaff').user.id
            )
            # self.db.add_bill_detail_to_db(_cur_bill)
            bills.append(_cur_bill)
        self.db.add_bills_to_db(bills)

    def do_payment(self):
        if not self.data:
            toast("Empty Order")
            return
        else:
            if not self._code:
                # Pay for Instance Order
                self.generate_curr_bill_code()
                self._insert_to_bills()
                self._code = ""
                self.data = []
                toast("Pay for Instance Order")
            else:
                # Pay for Order Stored
                self.db.delete_order_detail_by_code(self._code)
                self._insert_to_bills()
                self._code = ""
                self.data = []
                MDApp.get_running_app().root.get_screen("salesstaff").show_ordered()
                toast("Pay for Ordered")

    def save_order_toPay_later(self):
        if not self.data:
            toast("Empty Order")
            return
        else:
            if not self._code:
                self.generate_curr_bill_code()
                # save NEW Order to Pay later
                self._insert_to_orders()
                self._code = ""
                self.data = []
                toast("New Order Saved")
            else:
                # save EDITED Order to Pay later
                self.db.delete_order_detail_by_code(self._code)
                self._insert_to_orders()
                self._code = ""
                self.data = []
                toast("Edited Order Saved")
            MDApp.get_running_app().root.get_screen("salesstaff").show_ordered()

    def _insert_to_orders(self):
        user = MDApp.get_running_app().root.get_screen("salesstaff").user
        orders = []
        for order in self.data:
            _cur_order = model.Order(
                code=self._code,
                quantity=order["quantity"],
                price=order["price"],
                product=order["name"],
                cashier_id=user.id
            )
            # self.db.add_order_detail_to_db(_cur_order)
            orders.append(_cur_order)
        self.db.add_orders_to_db(orders)

    def reduce_quantity(self, item_bill):
        for item in self.data:
            if item["name"] == item_bill.name:
                if item["quantity"] > 1:
                    item["quantity"] -= 1
                    self._update()

    def raise_quantity(self, item_bill):
        for item in self.data:
            if item["name"] == item_bill.name:
                item["quantity"] += 1
                self._update()

    def delete_item(self, item_bill):
        for item in self.data:
            if item["name"] == item_bill.name:
                self.data.remove(item)
                # self.refresh_from_data()

    def check_item(self, item_add):
        for item in self.data:
            if item["name"] == item_add["name"]:
                return False
        return True

    def add_item(self, item):
        if self.check_item(item):
            self.data.append(item)


class BillListItem(MDCard):
    image = StringProperty()
    name = StringProperty()
    quantity = NumericProperty(1)
    price = NumericProperty(0.0)
    bg_color = ColorProperty([0, 0, 0, 0])

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

    def _minus_amount(self):
        self.parent.parent.reduce_quantity(self)
        # if self.quantity > 1:
        #    self.quantity -= 1

    def _plus_amount(self):
        self.parent.parent.raise_quantity(self)
        #self.quantity += 1

    def _delete_item(self):
        self.parent.parent.delete_item(self)
