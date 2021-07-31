import os
import shutil
import stat

from kivy.lang import Builder

# utils.load_kv("root.kv")


def load_kv(file_name, file_path=os.path.join("libs", "uix", "kv")):
    with open(os.path.join(file_path, file_name), encoding="utf-8") as kv:
        Builder.load_string(kv.read())


'''
with open(os.path.join(TEMPLATES_FOLDER, "classes.json")) as f:
            data = json.loads(f.read())

utils.edit_file(
    file=os.path.join(FULL_PATH_TO_PROJECT, "hotreloader.py"),
    values={
        "CLASSES": f"CLASSES = {str(data[self.selected_template])}"
    },
)
'''


def edit_file(file, values=None):

    with open(file) as f:
        string_file = f.read()

    if values:
        for key in values.keys():
            if not values[key]:
                continue
            string_file = string_file.replace(key, values[key])

        with open(file, "w") as f:
            f.write(string_file)


'''
for file in utils.get_files(FULL_PATH_TO_PROJECT, [".py", ".spec"]):
    utils.edit_file(
        file=file,
        values={
            "APPLICATION_TITLE": APPLICATION_TITLE,
            "PROJECT_NAME": PROJECT_NAME,
            "project_name": project_name,
            "APPLICATION_VERSION": APPLICATION_VERSION,
            "AUTHOR_NAME": AUTHOR_NAME,
            "PRIMARY_PALETTE": self.ids.primary.ids.primary_palette.current_item,  # NOQA: E501
            "PRIMARY_HUE": self.ids.primary.ids.primary_hue.current_item,  # NOQA: E501
            "ACCENT_PALETTE": self.ids.accent.ids.accent_palette.current_item,  # NOQA: E501
            "ACCENT_HUE": self.ids.accent.ids.accent_hue.current_item,
            "THEME_STYLE": self.ids.theme_style.ids.theme_style.current_item,  # NOQA: E501
        },
    )
'''


def get_files(path, ext):
    files = []

    for i in os.listdir(path):
        if os.path.splitext(i)[1] in ext:
            files.append(os.path.join(path, i))

    return files


'''
utils.copytree(BASE_TEMPLATE_FOLDER, FULL_PATH_TO_PROJECT)
'''


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except Exception:
                pass  # lchmod not available
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
