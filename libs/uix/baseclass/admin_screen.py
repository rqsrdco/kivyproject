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
from kivymd.uix.list import OneLineIconListItem
from kivymd.toast.kivytoast import toast
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dropdownitem import MDDropDownItem
import model


class AddRolePopup(Popup):

    def __init__(self, obj, **kwargs):
        super(AddRolePopup, self).__init__(**kwargs)
        self.title = ""
        self.lookback = obj

    def set_newRole(self):
        new_role = self.ids.text_field.text.strip()
        if new_role:
            if MDApp.get_running_app().root.db.add_new_role(new_role.capitalize()):
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
    gender_items = ListProperty([])
    role_items = ListProperty([])
    curr_staff_id = NumericProperty(-1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.init_gender_drop()
        self.init_role_drop()

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
        )
        self.gender_menu.bind()

    def set_gender_item(self, text_item):
        self.ids.drop_gender.set_item(text_item)
        self.gender_menu.dismiss()

    def on_pre_enter(self):
        Window.size = (1024, 768)
        Window.minimum_width, Window.minimum_height = Window.size

    def on_enter(self):
        self.get_staffs()

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
            ok = MDApp.get_running_app().root.db.create_staff_detail(data)
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
                ok = MDApp.get_running_app().root.db.update_staff_detail(self.curr_staff_id, data)
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
            ok = MDApp.get_running_app().root.db.delete_staff_detail(self.curr_staff_id)
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

    def change_state_toolbar(self, value):
        if value == 'normal':
            self.ids.contH1.state = 'normal'
            self.ids.contH2.state = 'normal'
            # self.ids.contH3.state = 'normal'

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
        data = MDApp.get_running_app().root.db.get_staff(self.admin_user)
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


class SongCover(MDBoxLayout):
    angle = NumericProperty()
    amin = Animation(angle=360, d=3, t='linear')
    amin += Animation(angle=0, d=0, t='linear')

    progress = Animation(value=100, d=100, t='linear')
    amin.repeat = True

    def rotate(self):
        if self.amin.have_properties_to_animate(self):
            self.amin.stop(self)
            self.progress.stop(self.widget)
        else:
            self.amin.start(self)
            self.progress.start(self.widget)

    def play(self, widget):
        self.widget = widget
        self.progress.start(widget)
        self.rotate()


class PopupLabelCell(Label):
    pass


class EditStatePopup(Popup):

    def __init__(self, obj, **kwargs):
        super(EditStatePopup, self).__init__(**kwargs)
        self.title = "Edit"
        self.populate_content(obj)

    def populate_content(self, obj):
        for x in range(len(obj.table_header.col_headings)):
            self.container.add_widget(PopupLabelCell(
                text=str(obj.table_header.col_headings[x])))
            textinput = TextInput(text=str(obj.row_data[x]))
            if x == 0:
                textinput.readonly = True
            self.container.add_widget(textinput)


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                  RecycleGridLayout):
    ''' Adds selection and focus behaviour to the view. '''

    selected_row = NumericProperty(0)
    obj = ObjectProperty(None)

    def get_nodes(self):
        nodes = self.get_selectable_nodes()
        if self.nodes_order_reversed:
            nodes = nodes[::-1]
        if not nodes:
            return None, None

        selected = self.selected_nodes
        if not selected:    # nothing selected, select the first
            self.selected_row = 0
            self.select_row(nodes)
            return None, None

        if len(nodes) == 1:     # the only selectable node is selected already
            return None, None

        last = nodes.index(selected[-1])
        self.clear_selection()
        return last, nodes

    def select_next(self, obj):
        ''' Select next row '''
        self.obj = obj
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if last == len(nodes) - 1:
            self.selected_row = nodes[0]
        else:
            self.selected_row = nodes[last + 1]

        self.selected_row += self.obj.total_col_headings
        self.select_row(nodes)

    def select_previous(self, obj):
        ''' Select previous row '''
        self.obj = obj
        last, nodes = self.get_nodes()
        if not nodes:
            return

        if not last:
            self.selected_row = nodes[-1]
        else:
            self.selected_row = nodes[last - 1]

        self.selected_row -= self.obj.total_col_headings
        self.select_row(nodes)

    def select_current(self, obj):
        ''' Select current row '''
        self.obj = obj
        last, nodes = self.get_nodes()
        if not nodes:
            return

        self.select_row(nodes)

    def select_row(self, nodes):
        col = self.obj.rv_data[self.selected_row]['range']
        for x in range(col[0], col[1] + 1):
            self.select_node(nodes[x])


class SelectableButton(RecycleDataViewBehavior, Button):
    ''' Add selection support to the Button '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''

        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            print("on_touch_down: self=", self)
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        self.text_size = self.size
        if index == rv.data[index]['range'][0]:
            self.halign = 'right'
        else:
            self.halign = 'left'


class HeaderCell(Label):
    pass


class TableHeader(ScrollView):
    """Fixed table header that scrolls x with the data table"""
    header = ObjectProperty(None)
    col_headings = ListProperty([])
    cols_minimum = DictProperty({})

    def __init__(self, **kwargs):
        super(TableHeader, self).__init__(**kwargs)
        self.db = lite.connect('local_database/db_sqlite/VietCupPOS.db')
        self.db_cursor = self.db.cursor()
        self.get_table_column_headings()

    def get_table_column_headings(self):
        self.db_cursor.execute("PRAGMA table_info(Bills)")
        col_headings = self.db_cursor.fetchall()

        print("col_heading", col_headings)
        for col_heading in col_headings:
            data_type = col_heading[2]

            if data_type == "integer":
                self.cols_minimum[col_heading[0]] = 49
            elif data_type == 'real':
                self.cols_minimum[col_heading[0]] = 100
            elif data_type == 'datetime':
                self.cols_minimum[col_heading[0]] = 120
            else:
                self.cols_minimum[col_heading[0]] = 180
            self.col_headings.append(col_heading[1])
            self.header.add_widget(HeaderCell(
                text=col_heading[1], width=self.cols_minimum[col_heading[0]]))


class RV(RecycleView):
    row_data = ()
    rv_data = ListProperty([])
    row_controller = ObjectProperty(None)
    total_col_headings = NumericProperty(0)
    cols_minimum = DictProperty({})
    table_header = ObjectProperty(None)

    def __init__(self, table_header, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.table_header = table_header
        self.total_col_headings = len(table_header.col_headings)
        self.cols_minimum = table_header.cols_minimum
        self.database_connection()
        self.get_states()
        Clock.schedule_once(self.set_default_first_row, .0005)
        self._request_keyboard()

    def database_connection(self):
        self.db = lite.connect('local_database/db_sqlite/VietCupPOS.db')
        self.db_cursor = self.db.cursor()

    def _request_keyboard(self):
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self, 'text'
        )
        if self._keyboard.widget:
            # If it exists, this widget is a VKeyboard object which you can use
            # to change the keyboard layout.
            pass
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'down':    # keycode[274, 'down'] pressed
            # Respond to keyboard down arrow pressed
            self.display_keystrokes(keyboard, keycode, text, modifiers)
            self.row_controller.select_next(self)

        elif keycode[1] == 'up':    # keycode[273, 'up] pressed
            # Respond to keyboard up arrow pressed
            self.display_keystrokes(keyboard, keycode, text, modifiers)
            self.row_controller.select_previous(self)

        # ctrl + e pressed
        elif len(modifiers) > 0 and modifiers[0] == 'ctrl' and text == 'e':
            # Respond to keyboard ctrl + e pressed, and call Popup
            self.display_keystrokes(keyboard, keycode, text, modifiers)
            self.on_keyboard_select()

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

    def display_keystrokes(self, keyboard, keycode, text, modifiers):
        print("\nThe key", keycode, "have been pressed")
        print(" - text is %r" % text)
        print(" - modifiers are %r" % modifiers)

    def on_keyboard_select(self):
        ''' Respond to keyboard event to call Popup '''

        # setup row data for Popup
        self.setup_row_data(
            self.rv_data[self.row_controller.selected_row]['Index'])

        # call Popup
        self.popup_callback()

    def on_mouse_select(self, instance):
        ''' Respond to mouse event to call Popup '''

        if self.row_controller.selected_row != instance.index:
            # Mouse clicked on row is not equal to current selected row
            self.row_controller.selected_row = instance.index

            # Hightlight mouse clicked/selected row
            self.row_controller.select_current(self)

        # setup row data for Popup
        self.setup_row_data(self.rv_data[instance.index]['Index'])

        # call Popup
        self.popup_callback()

        # enable keyboard request
        self._request_keyboard()

    def setup_row_data(self, value):
        self.db_cursor.execute(
            "SELECT * FROM Bills WHERE id=?", value)
        self.row_data = self.db_cursor.fetchone()

    def popup_callback(self):
        ''' Instantiate and Open Popup '''
        popup = EditStatePopup(self)
        popup.open()

    def set_default_first_row(self, dt):
        ''' Set default first row as selected '''
        self.row_controller.select_next(self)

    def get_states(self):
        self.db_cursor.execute(
            "SELECT * FROM Bills ORDER BY id ASC")
        rows = self.db_cursor.fetchall()

        data = []
        low = 0
        high = self.total_col_headings - 1
        for row in rows:
            for i in range(len(row)):
                data.append([row[i], row[0], [low, high]])
            low += self.total_col_headings
            high += self.total_col_headings
        for x in data:
            print(x)
        self.rv_data = [{'text': str(x[0]), 'Index': str(
            x[1]), 'range': x[2], 'selectable': True} for x in data]


class Table(BoxLayout):
    rv = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Table, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.header = TableHeader()
        self.rv = RV(self.header)

        self.rv.fbind('scroll_x', self.scroll_with_header)

        self.add_widget(self.header)
        self.add_widget(self.rv)

    def scroll_with_header(self, obj, value):
        self.header.scroll_x = value


class MyTable(BoxLayout):
    states_cities_or_areas = ObjectProperty(None)
    table = ObjectProperty(None)

    def display_states(self):
        self.remove_widgets()
        self.table = Table()
        self.states_cities_or_areas.add_widget(self.table)

    def remove_widgets(self):
        self.states_cities_or_areas.clear_widgets()
