from PIL import Image, ImageFont, ImageDraw
from PIL.ImageQt import toqpixmap
from PySide6.QtGui import QIcon

from configs import ICONS_FONT_FILE_PATH

FOLDER_SYM = "\uf114"
FOLDER_OPEN_SYM = "\uF115"
MINUS_SYM = "\ue800"
PLUS_SYM = "\ue801"
SEARCH_SYM = "\ue802"
CLOSE_SYM = "\ue805"
CONFIGS_SYM = "\uE804"
MERGE_SYM = "\uF1D9"
PICTURE_FILE_SYM = "\uF1C5"
PICTURE_SYM = "\uE807"
SYSTEM_SYM = "\uE803"
A_Z_SYM = "\uE808"
EDIT_SYM = "\uE80A"
ADJUST_SYM = "\uE809"
TRASH_BIN_SYM = "\uE80B"


def get_icon(symbol: str, font_size: int, font_color: tuple):
    """
    returns a transparent PIL image that contains the text
    symbol: the actual text
    font_size: the size of text
    color: the actual text
    """
    if type(symbol) is not str:
        raise TypeError("text must be a string")

    if len(symbol) != 1:
        raise TypeError("text must contain only one character")

    if type(font_size) is not int:
        raise TypeError("font_size must be a int")

    if type(font_color) is not tuple and len(font_color) != 3:
        raise TypeError("font_color must be a tuple of size 3")

    width = font_size + 5
    height = font_size + 5

    font = ImageFont.truetype(font=ICONS_FONT_FILE_PATH, size=font_size)
    image = Image.new(mode="RGBA", size=(width, height), color=(255, 255, 255, 0))

    draw = ImageDraw.Draw(im=image, mode="RGBA")
    draw.text(
        xy=(width / 2, height / 2), text=symbol, font=font, fill=font_color, anchor="mm"
    )

    return QIcon(toqpixmap(image))


def folder(size=16, color=(80, 76, 74)):
    return get_icon(FOLDER_SYM, size, color)


def minus(size=16, color=(80, 76, 74)):
    return get_icon(MINUS_SYM, size, color)


def plus(size=16, color=(80, 76, 74)):
    return get_icon(PLUS_SYM, size, color)


def search(size=16, color=(80, 76, 74)):
    return get_icon(SEARCH_SYM, size, color)


def close(size=16, color=(80, 76, 74)):
    return get_icon(CLOSE_SYM, size, color)


def configs(size=16, color=(80, 76, 74)):
    return get_icon(CONFIGS_SYM, size, color)


def open_folder(size=16, color=(80, 76, 74)):
    return get_icon(FOLDER_OPEN_SYM, size, color)


def merge(size=16, color=(80, 76, 74)):
    return get_icon(MERGE_SYM, size, color)


def picture_file(size=16, color=(80, 76, 74)):
    return get_icon(PICTURE_FILE_SYM, size, color)


def picture(size=16, color=(80, 76, 74)):
    return get_icon(PICTURE_SYM, size, color)


def trash_bin(size=16, color=(80, 76, 74)):
    return get_icon(TRASH_BIN_SYM, size, color)


def system(size=16, color=(80, 76, 74)):
    return get_icon(SYSTEM_SYM, size, color)


def a_z(size=16, color=(80, 76, 74)):
    return get_icon(A_Z_SYM, size, color)


def edit(size=16, color=(80, 76, 74)):
    return get_icon(EDIT_SYM, size, color)


def adjust(size=16, color=(80, 76, 74)):
    return get_icon(ADJUST_SYM, size, color)
