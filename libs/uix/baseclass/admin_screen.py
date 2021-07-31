import kivy
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation


class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self):
        Window.size = (636, 474)
        Window.minimum_width, Window.minimum_height = Window.size


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
