from kivy.core.text import LabelBase

fonts_path = "assets/fonts/"

fonts = [
    {
        "name": "Nunito",
        "fn_regular": fonts_path + "NunitoSans-Regular.ttf",
        "fn_bold": fonts_path + "NunitoSans-Bold.ttf",
        "fn_italic": fonts_path + "NunitoSans-Italic.ttf",
        "fn_bolditalic": fonts_path + "NunitoSans-BoldItalic.ttf",
    },
    {
        "name": "NunitoExtraLight",
        "fn_regular": fonts_path + "NunitoSans-ExtraLight.ttf",
        "fn_italic": fonts_path + "NunitoSans-ExtraLightItalic.ttf",
    },
    {
        "name": "NunitoLight",
        "fn_regular": fonts_path + "NunitoSans-Light.ttf",
        "fn_italic": fonts_path + "NunitoSans-LightItalic.ttf",
    },
    {
        "name": "NunitoSemiBold",
        "fn_regular": fonts_path + "NunitoSans-SemiBold.ttf",
        "fn_italic": fonts_path + "NunitoSans-SemiBoldItalic.ttf",
    },
    {
        "name": "NunitoExtraBold",
        "fn_regular": fonts_path + "NunitoSans-ExtraBold.ttf",
        "fn_italic": fonts_path + "NunitoSans-ExtraBoldItalic.ttf",
    },
    {
        "name": "NunitoBlack",
        "fn_regular": fonts_path + "NunitoSans-Black.ttf",
        "fn_italic": fonts_path + "NunitoSans-BlackItalic.ttf",
    },
    {
        "name": "Icons",
        "fn_regular": fonts_path + "materialdesignicons-webfont.ttf",
    },
]


def register_fonts():
    for font in fonts:
        LabelBase.register(**font)


font_styles = {
    "H1": ["NunitoLight", 96, False, -1.5],
    "H2": ["NunitoLight", 60, False, -0.5],
    "H3": ["Nunito", 48, False, 0],
    "H4": ["Nunito", 34, False, 0.25],
    "H5": ["Nunito", 24, False, 0],
    "H6": ["NunitoLight", 20, False, 0.15],
    "Subtitle1": ["NunitoBlack", 16, False, 0.15],
    "Subtitle2": ["NunitoLight", 14, False, 0.1],
    "Body1": ["Nunito", 16, False, 0.5],
    "Body2": ["Nunito", 14, False, 0.25],
    "Button": ["NunitoSemiBold", 14, True, 1.25],
    "Caption": ["Nunito", 12, False, 0.4],
    "Overline": ["Nunito", 10, True, 1.5],
    "Icon": ["Icons", 24, False, 0],
}
