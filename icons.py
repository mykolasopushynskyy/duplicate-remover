from PIL import Image, ImageFont, ImageDraw
from customtkinter import CTkImage

from configs import ICONS_FONT_FILE_PATH

FOLDER_SYM = "\uf114"
FOLDER_OPEN_SYM = "\uF115"
MINUS_SYM = "\ue800"
PLUS_SYM = "\ue801"
RUN_SYM = "\ue802"
SPINNER_SYM = "\ue838"
PICTURE_FILE_SYM = "\uF1C5"
UNSPECIFIED_FILE_SYM = "\uE803"
TEXT_FILE_SYM = "\uF0F6"
CONFIGS_SYM = "\uE804"
FILES_SYM = "\uF0C5"


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

    draw = ImageDraw.Draw(im=image)
    draw.text(xy=(width / 2, height / 2), text=symbol, font=font, fill=font_color, anchor="mm")

    photo_image = CTkImage(light_image=image, dark_image=image, size=(width, height))
    return photo_image


def folder(font_size=16, color=(0, 0, 0)):
    return get_icon(FOLDER_SYM, font_size, color)


def minus(font_size=16, color=(0, 0, 0)):
    return get_icon(MINUS_SYM, font_size, color)


def plus(font_size=16, color=(0, 0, 0)):
    return get_icon(PLUS_SYM, font_size, color)


def run(font_size=16, color=(0, 0, 0)):
    return get_icon(RUN_SYM, font_size, color)


def spinner(font_size=16, color=(0, 0, 0)):
    return get_icon(SPINNER_SYM, font_size, color)


def configs(font_size=16, color=(0, 0, 0)):
    return get_icon(CONFIGS_SYM, font_size, color)


def open_folder(font_size=16, color=(0, 0, 0)):
    return get_icon(FOLDER_OPEN_SYM, font_size, color)
