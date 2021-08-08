import os
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.screen import MDScreen
from kivymd.theming import ThemableBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.floatlayout import MDFloatLayout

from kivy.properties import NumericProperty, StringProperty, ColorProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as ColorHex
from kivy.clock import mainthread


class AuthorityScreen(ThemableBehavior, MDScreen):

    card_x = NumericProperty(0)
    bg_color = ColorProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.bg_color = self.theme_cls.divider_color

    def on_pre_enter(self):
        Window.size = (636, 474)
        Window.minimum_width, Window.minimum_height = Window.size

    def on_enter(self):
        self.animation_to_signin()

    def on_size(self, *args):
        if self.card_x:
            self.card_x = self.ids.box.width - self.ids.box2.width - dp(40)

    @mainthread
    def animation_to_getpwd(self):
        def animation_complete(*args):
            self.ids.box2.add_widget(ForgetpPasswordBox())
            Animation(scale=1, d=0.1).start(self.ids.box2.children[0])

        self.ids.box2.clear_widgets()
        Animation(scale=1, d=0.3).start(self.ids.auth_box_bg)
        Animation(scale=0, d=0.3).start(self.ids.forgotpwd_box_bg)
        animation = Animation(
            card_x=self.ids.box.width - self.ids.box2.width - dp(40),
            d=0.3,
            t="in_out_cubic",
        )
        animation.bind(on_complete=animation_complete)
        animation.start(self)
        self.ids.enter_getpwd.disabled = True
        self.ids.enter_signin.disabled = False
        self.ids.enter_signup.disabled = False

    @mainthread
    def animation_to_signup(self):
        def animation_complete(*args):
            self.ids.box2.add_widget(SignUpBox())
            Animation(scale=1, d=0.1).start(self.ids.box2.children[0])

        self.ids.box2.clear_widgets()
        Animation(scale=0, d=0.2).start(self.ids.auth_box_bg)
        Animation(scale=1, d=0.3).start(self.ids.forgotpwd_box_bg)
        animation = Animation(
            card_x=0,
            d=0.3,
            t="in_out_cubic",
        )
        animation.bind(on_complete=animation_complete)
        animation.start(self)
        self.ids.enter_getpwd.disabled = False
        self.ids.enter_signin.disabled = True
        self.ids.enter_signup.disabled = True

    @mainthread
    def animation_to_signin(self):
        def animation_complete(*args):
            self.ids.box2.add_widget(SignInBox())
            Animation(scale=1, d=0.1).start(self.ids.box2.children[0])

        self.ids.box2.clear_widgets()
        Animation(scale=0, d=0.2).start(self.ids.auth_box_bg)
        Animation(scale=1, d=0.3).start(self.ids.forgotpwd_box_bg)
        animation = Animation(
            card_x=0,
            d=0.3,
            t="in_out_cubic",
        )
        animation.bind(on_complete=animation_complete)
        animation.start(self)
        self.ids.enter_getpwd.disabled = False
        self.ids.enter_signin.disabled = True
        self.ids.enter_signup.disabled = True

    @mainthread
    def do_login(self, email, pwd):
        user = None
        try:
            user = self.manager.db.get_user_by_email(email)
        except Exception:
            pass
        if user is None or email != user.email:
            self.ids.box2.children[0].ids.email_field.text = ""
            self.ids.box2.children[0].ids.email_field.hint_text = "Invalid Email"
        else:
            if pwd == user.password:
                acc_type = user.role_id
                if acc_type == 2:
                    self.manager.set_current("administrator", side="right")
                    MDApp.get_running_app().get_date()
                    self.manager.get_screen(
                        "administrator").curr_date.text = MDApp.get_running_app().date
                else:
                    self.manager.set_current("salesstaff", side="right")
                    self.manager.get_screen("salesstaff").user = user.email
            else:
                self.ids.box2.children[0].ids.pwd_text_field.text = ""
                self.ids.box2.children[0].ids.pwd_text_field.hint_text = "Invalid Password"


class ScaleBox(MDBoxLayout):
    scale = NumericProperty(1)


class SignUpBox(ScaleBox):
    def next(self):
        self.ids.slide.load_next(mode='next')
        self.ids.name.text_color = MDApp.get_running_app().theme_cls.primary_color
        self.ids.progress.value = 100
        self.ids.progress.color = MDApp.get_running_app().theme_cls.primary_color
        self.ids.progress.type = "indeterminate"

        self.ids.btn_name.text_color = MDApp.get_running_app().theme_cls.primary_color
        #self.ids.btn_name.icon = "check-decagram"

    def next1(self):
        self.ids.slide.load_next(mode='next')
        self.ids.contact.text_color = MDApp.get_running_app().theme_cls.primary_color
        self.ids.progress1.value = 100
        self.ids.progress1.color = MDApp.get_running_app().theme_cls.primary_color
        self.ids.progress1.type = "indeterminate"

        self.ids.btn_contact.text_color = MDApp.get_running_app().theme_cls.primary_color
        #self.ids.btn_contact.icon = "check-decagram"

    def previous(self):
        self.ids.slide.load_previous()

        self.ids.progress.value = 0
        self.ids.progress.color = MDApp.get_running_app().theme_cls.divider_color
        self.ids.progress.type = "determinate"

        self.ids.name.text_color = MDApp.get_running_app().theme_cls.divider_color
        self.ids.btn_name.text_color = MDApp.get_running_app().theme_cls.divider_color
        self.ids.btn_name.icon = "account-network-outline"

    def previous1(self):
        self.ids.slide.load_previous()

        self.ids.progress1.value = 0
        self.ids.progress1.color = MDApp.get_running_app().theme_cls.divider_color
        self.ids.progress1.type = "determinate"

        self.ids.contact.text_color = MDApp.get_running_app().theme_cls.divider_color
        self.ids.btn_contact.text_color = MDApp.get_running_app().theme_cls.divider_color
        self.ids.btn_contact.icon = "card-account-phone-outline"


class ForgetpPasswordBox(ScaleBox):
    pass


class SignInBox(ScaleBox):

    def validate_account(self):
        if self.ids.email_field.text != "" and self.ids.pwd_text_field.text != "":
            self.parent.parent.do_login(
                self.ids.email_field.text, self.ids.pwd_text_field.text)
        else:
            if self.ids.email_field.text == "":
                self.ids.email_field.hint_text = "Email required"
            if self.ids.pwd_text_field.text == "":
                self.ids.pwd_text_field.hint_text = "Password required"
