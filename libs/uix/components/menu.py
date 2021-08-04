from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, NumericProperty, ObjectProperty, DictProperty
from kivymd.toast import toast
import json
from kivymd.app import MDApp
from kivy.clock import mainthread


Builder.load_string(
    """
<MenuCardItem>
    orientation: "vertical"
    # adaptive_size: True
    #size_hint: .5, None
    adaptive_height: True
    pos_hint: {"center_x": .5, "center_y": .5}
    padding: dp(6)
    elevation: 12
    focus_behavior: True
    ripple_behavior: True
    focus_color: app.theme_cls.ripple_color
    unfocus_color: app.theme_cls.divider_color
    md_bg_color: app.theme_cls.primary_color if root.selected else app.theme_cls.divider_color
    radius: [12]

    MDBoxLayout:
        id: box_top
        orientation: "horizontal"
        spacing: "6"
        padding: dp(6), dp(6), dp(6), dp(6)
        adaptive_size: True
        FitImage:
            source: root.image
            size_hint: None, None
            size: dp(68), dp(68)
            pos_hint: {"center_y": .5}

        MDBoxLayout:
            id: text_box
            orientation: "vertical"
            adaptive_width: True
            spacing: "10dp"

            MDLabel:
                text: root.name
                theme_text_color: "Primary"
                font_style: "Button"
                bold: True
                halign: "left"
                adaptive_height: True
                text_size: self.width, None

            MDLabel:
                text: str(root.price)
                halign: "left"
                adaptive_height: True
                text_size: self.width, None
                theme_text_color: "Primary"
    MDSeparator:

    MDBoxLayout:
        id: box_bottom
        adaptive_height: True
        spacing: dp(12)
        padding: dp(6), dp(6), dp(6), dp(6)

        MDLabel:
            text: str(root.quantity) if root._list_of_order else root.descriptions
            pos_hint: {"center_y": .5}
            theme_text_color: "Primary"
            halign: "center"
            adaptive_height: True
            text_size: self.width, None

<MenuRecycleView>
    canvas.before:
        Color:
            rgba: app.theme_cls.divider_color if self.data else app.theme_cls.accent_color
        RoundedRectangle:
            radius: [12]
            size: self.size
            pos: self.pos
    viewclass: 'MenuCardItem'
    bar_width: dp(0)
    SelectableRecycleGridLayout:
        padding: dp(6)
        spacing: dp(12)
        cols: 3
        default_size: None, dp(145)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        #multiselect: True
        #touch_multiselect: True
    """
)


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


class MenuRecycleView(RecycleView):
    _selected_item = DictProperty(None)
    _total_order = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MenuRecycleView, self).__init__(**kwargs)
        self.fake_data("coffee")

    @mainthread
    def take_order(self):
        self.data = []
        dbsql = MDApp.get_running_app().root.local_sqlite
        order_wait = dbsql.extractAllData('Orders', order_by='order_code')
        if not order_wait:
            toast("Orders sold out !")
            return
        else:
            _out_list = [[]]
            _code = order_wait[0][1]
            for i, item in enumerate(order_wait):
                if item[1] != _code and i != len(order_wait) - 1:
                    _code = item[1]
                    _out_list.append([])
                _out_list[-1].append(item)
            self._total_order = len(_out_list)
            for o in _out_list:
                _ma = o[0][1]
                _money = 0
                for k in o:
                    _money += round((k[3] * k[4]), 2)
                od = {
                    "name": _ma,
                    "quantity": round(_money, 2),
                    "price": len(o),
                    "image": "assets/images/order.png",
                    "_list_of_order": o
                    # "on_press": lambda x=json.dumps(Menu(
                    #    _ma,
                    #    round(_money, 2),
                    #    len(o),
                    #    "assets/images/order.png",
                    #    o
                    # )): self.set_curr(x)
                }
                self.data.append(od)

    @mainthread
    def fake_data(self, data):
        with open("assets/%s.json" % data, encoding='utf-8') as f:
            self.menu_data = json.load(f)

        self.data = []
        for i in self.menu_data:
            mn = {
                "name": i,
                # "quantity": 1,
                "descriptions": self.menu_data[i]["descriptions"],
                "price": self.menu_data[i]["price"],
                "image": self.menu_data[i]["image"],
                "_list_of_order": []
                # "on_press": lambda x=json.dumps(Menu(
                #    i,
                #    self.menu_data[i]["quantity"],
                #    self.menu_data[i]["price"],
                #    self.menu_data[i]["image"],
                #    []
                # )): self.set_curr(x)
            }
            self.data.append(mn)

    @mainthread
    def on_data(self, instance, data):
        self.refresh_from_data()

    def on__selected_item(self, *args):
        pass


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    selected_item = DictProperty(None)


class MenuCardItem(RecycleDataViewBehavior, MDCard):
    image = StringProperty()
    name = StringProperty()
    price = NumericProperty()
    descriptions = StringProperty('')
    quantity = NumericProperty(1)
    _list_of_order = ListProperty(None)
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(MenuCardItem, self).__init__(**kwargs)
        self._list_of_order = []

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(MenuCardItem, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(MenuCardItem, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if self.selected:
            rv._selected_item = rv.data[index]
            self.selected = False
