from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, StringProperty, NumericProperty, ObjectProperty, DictProperty
from kivymd.toast import toast
import json
from kivymd.app import MDApp
from kivy.clock import mainthread
from kivy.metrics import dp


Builder.load_string(
    """
<MenuCardItem>
    orientation: "vertical"
    #adaptive_size: True
    #size_hint: .5, None
    adaptive_height: True
    #pos_hint: {"center_x": .5, "center_y": .5}
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
            id: img
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
                size_hint_x: None
                width: root.width - img.width - dp(24)
                theme_text_color: "Primary"
                font_style: "Subtitle2"
                bold: True
                halign: "left"
                adaptive_height: True
                #text_size: self.width, None

            MDLabel:
                text: "{:,} item".format(root.price) if root._isOrder else "{:,.2f} vnd".format(root.price)
                halign: "left"
                adaptive_height: True
                text_size: self.width, None
                theme_text_color: "Primary"
                font_style: "Subtitle2"
    MDSeparator:

    MDBoxLayout:
        id: box_bottom
        adaptive_height: True
        spacing: dp(12)
        padding: dp(6), dp(6), dp(6), dp(6)
        MDLabel:
            text: "{:,.2f} vnd".format(float(root.descriptions)) if root._isOrder else root.descriptions
            pos_hint: {"center_y": .5}
            theme_text_color: "Primary"
            halign: "center"
            adaptive_height: True
            text_size: self.width, None
            font_style: "Caption"

<MenuRecycleView>
    rv_menu: rv_menu
    orientation: 'horizontal'
    #md_bg_color: app.theme_cls.primary_color
    RecycleView:
        id: rv_menu
        canvas.before:
            Color:
                rgba: app.theme_cls.divider_color
            RoundedRectangle:
                radius: [12]
                size: self.size
                pos: self.pos
        viewclass: 'MenuCardItem'
        data: root.data
        bar_width: dp(0)
        do_scroll_x: False
        RecycleGridLayout:
            cols: root.cols
            default_size: None, dp(152)
            default_size_hint: 1, None
            size_hint_y: None
            height: self.minimum_height
            padding: root.width * 0.02, root.height * 0.02
            spacing: min(root.width, root.height) * 0.02
    """
)


class Menu(dict):
    def __init__(self, name, quantity, price, image, isOrder):
        dict.__init__(
            self,
            name=name,
            quantity=quantity,
            price=price,
            image=image,
            _isOrder=isOrder
        )


class MenuRecycleView(MDBoxLayout):
    #_total_order = NumericProperty(0)
    #_selected_item = NumericProperty()
    #_menu_item = ObjectProperty(None)
    data = ListProperty()
    rv_menu = ObjectProperty()
    cols = NumericProperty(1)

    def __init__(self, **kwargs):
        super(MenuRecycleView, self).__init__(**kwargs)
        self.data = []

    @mainthread
    def on_data(self, instance, data):
        self.rv_menu.refresh_from_data()
        if data:
            if len(data) in [1, 2]:
                self.cols = 1
            elif len(data) == 3:
                self.cols = 2
            else:
                self.cols = 3
        else:
            pass


class MenuCardItem(RecycleDataViewBehavior, MDCard):
    image = StringProperty()
    descriptions = StringProperty('')
    name = StringProperty()
    price = NumericProperty()
    _isOrder = BooleanProperty(False)

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(MenuCardItem, self).__init__(**kwargs)

    # def refresh_view_attrs(self, rv, index, data):
    #    """ Catch and handle the view changes """
    #    self.index = index
    #    return super(MenuCardItem, self).refresh_view_attrs(rv, index, data)

    # def on_touch_down(self, touch):

    #    if super(MenuCardItem, self).on_touch_down(touch):
    #        return True
    #    if self.collide_point(*touch.pos) and self.selectable:
    #        return self.parent.select_with_touch(self.index, touch)

    # def apply_selection(self, rv, index, is_selected):
    #    ''' Respond to the selection of items in the view. '''
    #    self.selected = is_selected

    # def on_release(self):
    #    self.parent.parent._selected_item = self.index
