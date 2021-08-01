import os
import sys
import json
from kivy.factory import Factory
#
root_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]
sys.path.insert(0, os.path.join(root_dir, "libs", "applibs"))
sys.path.insert(0, os.path.join(root_dir, "libs", "uix"))
sys.path.insert(0, os.path.join(root_dir, "local_database"))
#
import traceback  # NOQA: E402
from kivymdapp import KivyMDApp  # NOQA: E402

"""
Registering factories from factory.json.
"""
r = Factory.register

with open("factory_registers.json") as fd:
    custom_widgets = json.load(fd)
    for module, _classes in custom_widgets.items():
        for _class in _classes:
            r(_class, module=module)


try:
    from kivy.resources import resource_add_path, resource_find
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    KivyMDApp().run()
except Exception:
    error = traceback.format_exc()

    with open("ERRORS.log", "w") as error_file:
        error_file.write(error)

    print(error)
