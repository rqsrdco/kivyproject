import json

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty
# SQLite
from databaseSQLite import DatabaseSQLite


class Root(ScreenManager):
    local_sqlite = ObjectProperty()
    previous_screen = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self._goto_previous_screen)
        self.local_sqlite = DatabaseSQLite()
        # Clock.schedule_once(self.add_screens)
        # getting screens data from screens.json
        with open("screens.json") as f:
            self.screens_data = json.load(f)

    def set_current(self, screen_name, side="left", quick=False):
        # checks that the screen already added to the screen-manager
        if not self.has_screen(screen_name):
            screen = self.screens_data[screen_name]
            # loads the kv file
            Builder.load_file(screen["kv"])
            # imports the screen class dynamically
            exec(screen["import"])
            # calls the screen class to get the instance of it
            screen_object = eval(screen["object"])
            # automatically sets the screen name using the arg that passed in set_current
            screen_object.name = screen_name
            # finnaly adds the screen to the screen-manager
            self.add_widget(screen_object)

        # saves previous screen information
        self.previous_screen = {"name": self.current, "side": side}
        # sets transition direction
        self.transition.direction = side
        # sets to the current screen
        self.current = screen_name

    def _goto_previous_screen(self, instance, key, *args):
        if key == 27:
            self.goto_previous_screen()
            return True

    def goto_previous_screen(self):
        if self.previous_screen:
            self.set_current(
                self.previous_screen["name"],
                side="right" if self.previous_screen["side"] == "left" else "left",
            )
            self.previous_screen = None

    def add_screens(self, interval):
        with open("screens.json") as f:
            screens = json.load(f)

        for screen_name in screens.keys():
            screen_details = screens[screen_name]
            Builder.load_file(screen_details["kv"])
            exec(screen_details["import"])  # excecuting imports
            screen_object = eval(screen_details["object"])  # calling it
            screen_object.name = screen_name  # giving the name of the screen
            self.add_widget(
                screen_object
            )
