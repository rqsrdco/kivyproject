"""
Allow the simple creation of kivy UIs for arbitrary python object.  The UI
will automatically update as the underlying python model changes, provided any
function on the UI side that changes the underlying data model use the 
"update" decorator.
"""

from kivy.lang import Builder
from kivy.event import EventDispatcher
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.app import App
import kivy
kivy.require('1.7.0')


##################
# DATA MODEL SIDE
##################

class DataModel(object):
    def __init__(self):
        self.a = 'This is a'
        self.b = 'This is b'

    @property
    def c(self):
        return self.a + '\nand\n' + self.b


# Create an instance of the data model that will be used in both the
#   data processing and UI display sides of things
common_data_model = DataModel()

##################
# BRIDGE
##################


class UI_DataModelMeta(type):
    def __new__(meta, name, bases, dct):
        # Create kivy StringProperty objects for all the attributes
        #   in the underlying data model
        added_attributes = []
        for attr in dir(common_data_model):
            if not attr.startswith('_'):
                # print "Making attribute %s" % attr
                assert attr not in dir(EventDispatcher())
                dct[attr] = StringProperty('INIT')
                added_attributes.append(attr)
        # Let the UI_DataModel know what attributes are from the common model
        dct['_model_attr'] = added_attributes
        return super(UI_DataModelMeta, meta).__new__(meta, name, bases, dct)


class UI_DataModel(EventDispatcher):
    __metaclass__ = UI_DataModelMeta

    def __getattribute__(self, key):
        # print ">> Trying to get %s" % key
        if key == '_model_attr':
            return object.__getattribute__(self, key)
        elif key in self._model_attr:
            # print "    INTERCEPTED!"
            # Get the value of this key from the common data model
            val = str(getattr(common_data_model, key))
            # print "  val is %s" % val
            # Invoke kivy's StringProperty setter by setting our attribute
            setattr(self, key, val)
            # Proceed as normal
            return EventDispatcher.__getattribute__(self, key)
        else:
            # print "    Pushing up to base class"
            return EventDispatcher.__getattribute__(self, key)

    def update(self, func):
        """Decorator to put around any UI function that update the common
           data model"""
        def wrapper(*args, **kwargs):
            # Execute function as normal
            ret = func(*args, **kwargs)
            # Update UI Data Model wrapper
            for attr in self._model_attr:
                getattr(self, attr)
            return ret
        return wrapper


##################
# UI SIDE
##################

Builder.load_string("""
<RootWidget>:
    cols: 2
    Label:
        text: "Attribute a:"
    Label:
        text: root.ui_data_model.a
    Label:
        text: "Attribute b:"
    Label:
        text: root.ui_data_model.b
    Label:
        text: "Attribute c:"
    Label:
        text: root.ui_data_model.c
    Button:
        text: "Make data_model.a longer"
        on_press: root.button_press()
    Button:
        text: "Make data_model.b shorter"
        on_press: root.button_press2()
""")


class RootWidget(GridLayout):
    ui_data_model = UI_DataModel()

    @ui_data_model.update
    def button_press(self, *args):
        # Make sure you modify the common data model, not the UI's
        #  data model wrapper
        common_data_model.a = 'This is a and it is really long now'
        # print common_data_model.c
        # print self.ui_data_model.c
        # print self.ui_data_model.a

    @ui_data_model.update
    def button_press2(self, *args):
        common_data_model.b = 'B'
        # print common_data_model.c
        # print self.ui_data_model.c


class TestApp(App):
    def build(self):
        return RootWidget()


app = TestApp()
app.run()
