from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivymd.app import MDApp


Builder.load_string(
    """
<AddPopup>
    size_hint: 0.8, 0.8
    title: "Add Asset"
    title_size: root.height * 0.05
    auto_dismiss: False
    BoxLayout:
        orientation: 'vertical'
        GridLayout:
            rows: 5
            cols: 2
            padding: root.width * 0.02, root.height * 0.02
            spacing: min(root.width, root.height) * 0.02

            Label:
                id: asset_name_label
                text: "Asset name"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            TextInput:
                id: asset_name
                text: "Asset name"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            Label:
                id: asset_price_label
                text: "Asset price"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            TextInput:
                id: asset_price
                text: "asset"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            Label:
                id: asset_amount_label
                text: "Asset amount"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            TextInput:
                id: asset_amount
                text: "Asset amount"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            Label:
                id: currency_label
                text: "Asset currency"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            TextInput:
                id: currency
                text: "currency"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            Label:
                id: asset_class_label
                text: "Asset class"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
            TextInput:
                id: asset_class
                text: "Asset class"
                halign: "center"
                font_size: root.height/25
                text_size: self.width, None
                center_y: .5
        Button:
            text: "Save"
            size_hint: 1, None
            height: root.height / 8
            on_release: root.save_asset()
        Button:
            text: "close"
            size_hint: 1, None
            height: root.height / 8
            on_release: root.dismiss()
    """
)


class AddPopup(Popup):
    """Popup for adding asset"""
    asset_name = ObjectProperty
    asset_price = ObjectProperty
    asset_amount = ObjectProperty
    currency = ObjectProperty
    asset_class = ObjectProperty
    wrapped_button = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super(AddPopup, self).__init__(*args, **kwargs)

    def open(self, correct=True):
        super(AddPopup, self).open(correct)

    def save_asset(self):
        # Make sure no input is empty
        if self.ids.asset_name.text.strip() and self.ids.asset_price.text.strip()\
                and self.ids.asset_amount.text.strip() and self.ids.currency.text.strip()\
                and self.ids.asset_class.text.strip():
            MDApp.get_running_app().root.current_screen.rv_data_global.append(
                {'text': self.ids.asset_name.text.strip()})
            MDApp.get_running_app().root.current_screen.rv_data_global.append(
                {'text': self.ids.asset_amount.text.strip(
                )})
            MDApp.get_running_app().root.current_screen.rv_data_global.append(
                {'text': self.ids.asset_price.text.strip()})
            self.dismiss()
