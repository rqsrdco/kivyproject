import re
import sqlite3 as lite
from datetime import datetime
from kivy.uix.recycleview import RecycleView
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.button import Button
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty, ListProperty, ObjectProperty, NumericProperty, DictProperty, StringProperty
import kivy
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, NoTransition
from kivy.animation import Animation
from kivy.uix.behaviors import ToggleButtonBehavior, ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.carousel import Carousel
from kivy.uix.screenmanager import ScreenManager

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from ripplebehavior import RectangularRippleBehavior
from kivymd.uix.card import MDCard
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast.kivytoast import toast
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dropdownitem import MDDropDownItem
import model
from kivymd.uix.list import TwoLineAvatarListItem, OneLineListItem, OneLineIconListItem
from kivymd.uix.expansionpanel import MDExpansionPanelThreeLine, MDExpansionPanel
#from kivy.event import EventDispatcher


class MenuContent(MDBoxLayout):
    _menu_item = ObjectProperty()
    _inventory = ObjectProperty()

    def save_menu_edited_item(self, txt_field):
        menu = self._menu_item["Menu"]
        if len(txt_field) >= 1 and float(txt_field) != menu.sell_price:
            data = model.Menu(
                id=menu.id,
                product_id=menu.product_id,
                sell_price=round(float(txt_field), 2)
            )
            kq = MDApp.get_running_app().root.db.update_menu_item(data)
            if kq:
                self._inventory.get_menu_by_category(
                    self._menu_item["Category"])

    def delete_menu_content(self):
        kq = MDApp.get_running_app().root.db.delete_menu_content(
            self._menu_item["Menu"])
        if kq:
            self._inventory.get_menu_by_category(
                self._menu_item["Category"])


class StoreContent(MDBoxLayout):
    _store_item = ObjectProperty()
    _inventory = ObjectProperty()

    # def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
    #    self.register_event_type("on_save_edit")

    def _check_int_txt(self, txt: str, value: int):
        if len(txt) >= 1 and int(txt) != value:
            return True
        else:
            return False

    def _check_float_txt(self, txt: str, value: float):
        if len(txt) >= 1 and float(txt) != value:
            return True
        else:
            return False

    def save_store_edited_item(self, price, qty):
        store = self._store_item["Store"]
        if self._check_float_txt(price, store.input_price) or self._check_int_txt(qty, store.quantity):
            data = model.Store(
                id=store.id,
                product_id=store.product_id,
                input_price=round(float(price), 2),
                quantity=int(qty)
            )
            kq = MDApp.get_running_app().root.db.update_store_item(data)
            if kq:
                self._inventory.get_store_by_category(
                    self._store_item["Category"])

    def delete_store_content(self):
        kq = MDApp.get_running_app().root.db.delete_store_content(
            store=self._store_item["Store"])
        if kq:
            self._inventory.get_store_by_category(
                self._store_item["Category"])


class InventoryPart(MDBoxLayout):
    categories = ListProperty()
    category_items = ListProperty()
    product_items = ListProperty()
    _curr_Product = ObjectProperty(None, allownone=True)
    _curr_categories = ObjectProperty(None)
    _pc = ObjectProperty(None, allownone=True)

    def show_add_itemMenu(self):
        self._curr_Product = None
        self.ids.p_name.text = ''
        self.ids.sell_price_menu.text = ''
        self.ids.sell_price_menu.error = False
        self.ids.sell_price_menu.focus = False
        if self.ids.add_itemMenu.height == 0:
            self.ids.add_itemMenu.height = self.height - dp(52)
        else:
            self.ids.add_itemMenu.height = 0

    def show_add_itemStore(self):
        self._curr_Product = None
        self.ids.txt_name_store.text = ''
        self.ids.input_price_store.text = ''
        self.ids.input_price_store.focus = False
        self.ids.input_price_store.error = False
        self.ids.qty_number.text = ''
        self.ids.qty_number.error = False
        self.ids.qty_number.focus = False
        if self.ids.add_itemStore.height == 0:
            self.ids.add_itemStore.height = self.height - dp(52)
        else:
            self.ids.add_itemStore.height = 0

    def get_product_byCategory(self, *args):
        db = MDApp.get_running_app().root.db
        results = None
        if args:
            results = db.get_ALlproduct_with_category(args[1])
        else:
            results = db.get_ALlproduct_with_category()

        if results is not None:
            self.ids.ls_products.clear_widgets()
            for i in results:
                self.ids.ls_products.add_widget(
                    ProductItem(
                        product=i["Product"],
                        category=i["Category"],
                        on_press=lambda x=i: self.show_currProduct(x)
                    )
                )

    def rv_set_category(self, value):
        self.ids.product_category.text = value.name
        self.ids.rv_category.data = []

    def set_list_categories(self, text="", search=False):
        def add_category_item(category):
            self.ids.rv_category.data.append(
                {
                    "viewclass": "IconListItem",
                    "icon": "format-list-bulleted-type",
                    "text": category.name,
                    "on_press": lambda x=category: self.rv_set_category(x),
                }
            )

        self.ids.rv_category.data = []
        for c in self.categories:
            if search:
                if text in c.name:
                    add_category_item(c)
            else:
                add_category_item(c)

    def delete_curr_product(self):
        if self._pc is not None:
            db = MDApp.get_running_app().root.db
            kq = db.delete_product(self._pc.product)
            if kq:
                self.get_product_byCategory(1, self._pc.category)
                self._pc = None
                self.ids.product_name.text = ''
                self.ids.product_category.text = ''

    def show_currProduct(self, value):
        self._pc = value
        self.ids.product_name.text = value.product.name
        self.ids.product_category.text = value.category.name

    def init_category_list(self):
        self.ids.ls_category.add_widget(IconListItem(
            icon="format-list-bulleted-type",
            text="All Product",
            on_press=lambda x: self.get_product_byCategory()
        ))
        if self.categories:
            for category in self.categories:
                self.ids.ls_category.add_widget(IconListItem(
                    icon="format-list-bulleted-type",
                    text=f"{category.name}",
                    on_press=lambda x=category, y=category: self.get_product_byCategory(
                        x, y)
                ))

    def init_category_drop(self, **kwargs):
        self.categories = kwargs["db"].get_category()
        self.init_category_list()
        self.category_items = [
            {
                "text": f"{c.name}",
                "viewclass": "IconListItem",
                "icon": "format-list-bulleted-type",
                "height": dp(52),
                "on_release": lambda x=c: self.set_category_item(x)
            } for c in self.categories
        ]
        self.category_menu = MDDropdownMenu(
            caller=self.ids.drop_category,
            items=self.category_items,
            position="bottom",
            width_mult=3,
            # elevation=12,
            # radius=[12,12,12,12]
        )

    def set_category_item(self, category_item):
        self._curr_categories = category_item
        self.ids.drop_category.set_item(category_item.name)

        self.get_menu_by_category(category_item)
        self.get_store_by_category(category_item)
        self.get_product_list(category_item)

        self.category_menu.dismiss()

    def set_currP(self, *args):
        self._curr_Product = args[1].product
        if args[0] == 1:
            self.ids.p_name.text = args[1].product.name
            self.ids.txt_name_store.text = ''
        else:
            self.ids.txt_name_store.text = args[1].product.name
            self.ids.p_name.text = ''

    def get_product_list(self, category_item):
        self.product_items = MDApp.get_running_app(
        ).root.db.get_product_by_category(category_item)
        if self.product_items:
            self.ids.container_menu_product.clear_widgets()
            self.ids.container_store_product.clear_widgets()
            for p in self.product_items:
                item = ProductItem(
                    product=p,
                    on_press=lambda x=p: self.set_currP(1, x)
                )
                self.ids.container_menu_product.add_widget(item)
                item1 = ProductItem(
                    product=p,
                    on_press=lambda x=p: self.set_currP(2, x)
                )
                self.ids.container_store_product.add_widget(item1)

    def add_product_toStore(self):
        if self._curr_Product is None:
            self.ids.txt_name_store.text = 'choose a product'
            toast("Choose a Product")
        elif self.ids.input_price_store.text == '':
            self.ids.input_price_store.error = True
            self.ids.input_price_store.focus = True
        elif self.ids.qty_number.text == '':
            self.ids.input_price_store.focus = False
            self.ids.input_price_store.error = False
            self.ids.qty_number.error = True
            self.ids.qty_number.focus = True
        else:
            db = MDApp.get_running_app().root.db
            if not db.check_product_exist_in_store(self._curr_Product):
                i_price = round(float(self.ids.input_price_store.text), 2)
                qty = int(self.ids.qty_number.text)
                store = model.Store(
                    product_id=self._curr_Product.id,
                    input_price=i_price,
                    quantity=qty
                )
                db.add_item_to_store(store)
                self.show_add_itemStore()
                self.get_store_by_category(self._curr_categories)
            else:
                toast("already exist")

    def add_product_toMenu(self):
        if self._curr_Product is None:
            self.ids.p_name.text = 'Choose a Product'
            toast("Choose a Product")
        elif self.ids.sell_price_menu.text == '':
            self.ids.sell_price_menu.error = True
            self.ids.sell_price_menu.focus = True
            toast("Enter Selling Price")
        else:
            self.ids.sell_price_menu.error = False
            self.ids.sell_price_menu.focus = False
            db = MDApp.get_running_app().root.db
            if not db.check_product_exist_in_menu(self._curr_Product):
                price = round(float(self.ids.sell_price_menu.text), 2)
                menu = model.Menu(
                    product_id=self._curr_Product.id, sell_price=price)
                db.add_item_to_menu(menu)
                self.show_add_itemMenu()
                self.get_menu_by_category(self._curr_categories)
            else:
                toast("already exist")

    def get_menu_by_category(self, category):
        menu = MDApp.get_running_app().root.db.get_menu_width_category(category)
        self.ids.container_menu.clear_widgets()
        for p in menu:
            name = p["Product"].name
            price = p["Menu"].sell_price
            self.ids.container_menu.add_widget(
                MDExpansionPanel(
                    icon=f"assets/images/product/{name}.png",
                    content=MenuContent(
                        _menu_item=p,
                        _inventory=self
                    ),
                    panel_cls=MDExpansionPanelThreeLine(
                        text=f"{name}",
                        secondary_text=f"{category.name}",
                        tertiary_text=f"{price} vnd",
                    )
                )
            )

    def get_store_by_category(self, category):
        store = MDApp.get_running_app().root.db.get_store_width_category(category)
        self.ids.container_store.clear_widgets()
        for p in store:
            name = p["Product"].name
            quantity = p["Store"].quantity
            price = p["Store"].input_price
            self.ids.container_store.add_widget(
                MDExpansionPanel(
                    icon=f"assets/images/product/{name}.png",
                    content=StoreContent(
                        _store_item=p,
                        _inventory=self
                    ),
                    panel_cls=MDExpansionPanelThreeLine(
                        text=f"{name}",
                        secondary_text=f"{quantity}",
                        tertiary_text=f"{price} vnd",
                    )
                )
            )


class StaffPart(MDBoxLayout):
    gender_items = ListProperty([])
    role_items = ListProperty([])
    curr_staff_id = NumericProperty(-1)
    _home = ObjectProperty()

    def init_role_drop(self):
        roles = MDApp.get_running_app().root.db.get_roles()
        if roles:
            self.role_items = [
                {
                    "viewclass": "IconListItem",
                    "icon": "account-cash" if i.role == "Cashier" else "account-cog" if i.role == "Administrator" else "security" if i.role == "Security" else "human-baby-changing-table" if i.role == "Waiter" else "card-account-details-star",
                    "text": f"{i.role}",
                    "height": dp(52),
                    "on_release": lambda x=f"{i.role}": self.set_role_item(x),
                } for i in roles
            ]
        self.role_menu = MDDropdownMenu(
            caller=self.ids.drop_role,
            items=self.role_items,
            position="center",
            width_mult=4,
            # elevation=12,
            # radius=[12,12,12,12]
        )
        self.role_menu.bind()

    def set_role_item(self, text_item):
        self.ids.drop_role.set_item(text_item)
        self.role_menu.dismiss()

    def init_gender_drop(self):
        self.gender_items = [
            {
                "viewclass": "IconListItem",
                "icon": "gender-female" if i == "Female" else "gender-male" if i == "Male" else "gender-male-female-variant",
                "text": f"{i}",
                "height": dp(52),
                "on_release": lambda x=f"{i}": self.set_gender_item(x),
            } for i in ["Male", "Female", "XY"]
        ]
        self.gender_menu = MDDropdownMenu(
            caller=self.ids.drop_gender,
            items=self.gender_items,
            position="center",
            width_mult=3,
            # elevation=12,
            #radius=[12, 12, 12, 12]
        )
        self.gender_menu.bind()

    def set_gender_item(self, text_item):
        self.ids.drop_gender.set_item(text_item)
        self.gender_menu.dismiss()

    def check_validate_field(self, instance, **obj):
        if instance.text == '':
            instance.error = True
            instance.focus = True
        else:
            instance.error = False
            instance.focus = False
            if obj["next"] is not None:
                obj["next"].focus = True

    def check_staff_fields(self):
        _validate = True
        _widgets = self.ids.container_infos.children
        for i in _widgets:
            if isinstance(i, MDTextField):
                if i.text == "":
                    i.error = True
                    i.focus = True
                    self.ids.member_seen.text = '%s requied' % i.hint_text
                    _validate = False
                    pass
                else:
                    i.error = False
                    i.focus = False
            elif isinstance(i, MDDropDownItem):
                if i.current_item == '':
                    self.ids.member_seen.text = 'Please choose %s' % i.text
                    _validate = False
                    pass
            elif isinstance(i, BoxLayout):
                for k in i.children:
                    if isinstance(k, MDDropDownItem):
                        if k.current_item == '':
                            self.ids.member_seen.text = 'Please choose %s' % k.text
                            _validate = False
                            pass
            else:
                pass
        return _validate

    def save_new_staff(self):
        _isValidate = self.check_staff_fields()
        if _isValidate:
            data = dict(
                email=self.ids.email.text,
                password=self.ids.pwd.text,
                first_name=self.ids.first_name.text,
                last_name=self.ids.last_name.text,
                phone_number=self.ids.phone.text,
                gender=self.ids.drop_gender.current_item,
                role_id=self.ids.drop_role.current_item
            )
            ok = self._home.manager.db.create_staff_detail(data)
            if ok:
                self.reset_infos_fields()
                self.get_staffs()
                toast("Successfully created")
            else:
                toast("Create Failed")

    def save_edited_staff(self):
        if self.curr_staff_id == -1:
            self.ids.member_seen.text = 'Please select a staff member to edit'
            toast("Please select a staff member to edit")
        else:
            if self.check_staff_fields():
                data = dict(
                    email=self.ids.email.text,
                    password=self.ids.pwd.text,
                    first_name=self.ids.first_name.text,
                    last_name=self.ids.last_name.text,
                    phone_number=self.ids.phone.text,
                    gender=self.ids.drop_gender.current_item,
                    role_id=self.ids.drop_role.current_item
                )
                ok = self._home.manager.db.update_staff_detail(
                    self.curr_staff_id, data)
                if ok:
                    self.reset_infos_fields()
                    self.get_staffs()
                    toast("Successfully updated")
                else:
                    toast("Update Failed")

    def delete_staff_detail(self):
        if self.curr_staff_id == -1:
            self.ids.member_seen.text = 'Please select a staff member to Delete'
            toast("Please select a staff member to Delete")
        else:
            ok = self._home.manager.db.delete_staff_detail(self.curr_staff_id)
            if ok:
                self.reset_infos_fields()
                self.get_staffs()
                toast("Successfully deleted")
            else:
                toast("Delete Failed")

    def reset_infos_fields(self):
        self.curr_staff_id = -1

        self.ids.email.text = ''
        self.ids.pwd.text = ''
        self.ids.first_name.text = ''
        self.ids.last_name.text = ''
        self.ids.phone.text = ''
        self.ids.drop_gender.current_item = ''
        self.ids.drop_role.current_item = ''
        self.ids.member_seen.text = ''

    def show_staff_infos(self, instance):
        self.curr_staff_id = instance._staff.id

        self.ids.email.text = instance._staff.email
        self.ids.pwd.text = instance._staff.password
        self.ids.first_name.text = instance._staff.first_name
        self.ids.last_name.text = instance._staff.last_name
        self.ids.phone.text = instance._staff.phone_number
        self.ids.drop_gender.set_item(instance._staff.gender)
        self.ids.drop_role.set_item(instance._staff.role.role)
        now = datetime.now()
        dt = "{} year || {} day".format(
            divmod((now-instance._staff.created_at).total_seconds(), 31536000)[0], (now-instance._staff.created_at).days)
        self.ids.member_seen.text = dt

    def get_staffs(self):
        data = self._home.manager.db.get_staff(self._home.admin_user)
        if data is not None:
            self.ids.staff_list.clear_widgets()
            for d in data:
                item = StaffItem(_staff=d)
                item.bind(on_press=self.show_staff_infos)
                self.ids.staff_list.add_widget(item)

    def addrole_callback(self):
        ''' Instantiate and Open Popup '''
        popup = AddRolePopup(self)
        popup.open()


class ProductItem(TwoLineAvatarListItem):
    product = ObjectProperty()
    category = ObjectProperty(None)


class AddRolePopup(Popup):

    def __init__(self, obj, **kwargs):
        super().__init__(**kwargs)
        self.title = ""
        self.lookback = obj

    def set_newRole(self):
        new_role = self.ids.text_field.text.strip()
        if new_role:
            if self.lookback._home.manager.db.add_new_role(new_role.capitalize()):
                self.dismiss()
                # load new to drop
                self.lookback.init_role_drop()
                toast("Successfully Added New")
            else:
                toast(new_role.capitalize() + ' ' + 'already exists')
        else:
            toast("You did not enter content")


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class StaffItem(MDCard):
    _staff = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elevation = 12


class Ripplebtn(RectangularRippleBehavior, MDLabel):
    pass


class TitleButtons(ToggleButtonBehavior, Ripplebtn):
    def __init__(self, **kwargs):
        super(TitleButtons, self).__init__(**kwargs)
        self.group = 'menu'
        self.size_hint = None, None
        self.height = 100

    def on_state(self, widget, state):
        if state == 'down':
            anim = Animation(rgba=(0, 52/255, 102/255, .3))
            anim.start(self.canvas.get_group('a')[0])
            self.font_style = 'Button'
            self.color = 0, 52/255, 102/255, 1
        else:
            anim = Animation(rgba=(0, 52/255, 102/255, 0), t='out_cubic')
            anim.start(self.canvas.get_group('a')[0])
            self.font_style = 'Button'
            self.color = 0, 0, 0, 1


class CointainerHeaders(ToggleButtonBehavior, BoxLayout):
    list_widgets = ListProperty()
    icon = StringProperty()
    text = StringProperty()
    icon1 = StringProperty('menu-down')
    color = ListProperty([.45, .56, .67, .83])

    def __init__(self, **kwargs):
        super(CointainerHeaders, self).__init__(**kwargs)

    def on_state(self, inst, value):
        if value == 'down':
            self.show()
            self.icon1 = 'menu-up'
            self.parent.parent.parent.state = 'down'

        else:
            self.unshow()
            self.icon1 = 'menu-down'

    def on_size(self, *args):
        try:
            self.ids.sm_main.transition = NoTransition()

            if self.width < dp(220):
                self.ids.sm_main.current = 'one'

            elif self.width > dp(220):
                self.ids.sm_main.current = 'two'
        except Exception:
            pass

    def show(self):
        self.color = 0, 52/255, 102/255, 1
        for wid in self.list_widgets:
            wid.halign = 'left'
            wid.padding_x = dp(39)
            wid.shorten = True
            wid.shorten_from = 'right'
            self.add_widget(wid, state='new')
            self.height += wid.height

    def unshow(self):
        self.color = 0, 0, 0, .83
        for wid in self.list_widgets:
            self.remove_widget(wid)
            self.height -= wid.height

    def add_widget(self, widget, index=0, state=None, canvas=None):
        if state is None and isinstance(widget, BoxLayout) is False:
            self.list_widgets.append(widget)
        else:
            return super(CointainerHeaders, self).add_widget(widget, index, canvas)


class LeftPanel(ToggleButtonBehavior, MDBoxLayout):
    def on_state(self, inst, value):
        if value == 'down':
            anim = Animation(width=dp(230), t='in_cubic', duration=.3)
            anim.start(self)
        else:
            anim = Animation(width=dp(68), t='out_cubic', duration=.3)
            anim.start(self)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            self.state = 'normal'
        else:
            return super(LeftPanel, self).on_touch_down(touch)


class AdminScreen(Screen):
    admin_user = ObjectProperty()
    line_nav = BooleanProperty(False)
    sm_content = ObjectProperty()

    inventory_part = ObjectProperty()
    staff_part = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.staff_part._home = self

        self.staff_part.init_gender_drop()
        self.staff_part.init_role_drop()
        # self.inventory_part.init_list_product(self)

    def on_pre_enter(self):
        Window.size = (1024, 768)
        Window.minimum_width, Window.minimum_height = Window.size
        self.inventory_part.init_category_drop(db=self.manager.db)

    def on_enter(self):
        self.staff_part.get_staffs()

    def change_state_toolbar(self, value):
        if value == 'normal':
            self.ids.contH1.state = 'normal'
            self.ids.contH2.state = 'normal'
            # self.ids.contH3.state = 'normal'
