import io
from tkinter import PhotoImage

from PIL import Image, ImageFont, ImageDraw

from configs import ICONS_FONT_FILE_PATH

FOLDER_SYM = "\uf114"
MINUS_SYM = "\ue800"
PLUS_SYM = "\ue801"
RUN_SYM = "\ue802"
SPINNER_SYM = "\ue838"


def image_to_byte_array(image: Image) -> bytes:
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes.read()


def get_icon(symbol, font_size, color):
    """
    returns a transparent PIL image that contains the text
    txt: the actual text
    font_size: the size of text
    color: the actual text
    """
    if type(symbol) is not str:
        raise TypeError("text must be a string")

    if len(symbol) != 1:
        raise TypeError("text must contain only one character")

    if type(font_size) is not int:
        raise TypeError("font_size must be a int")

    width = font_size + 5
    height = font_size + 5

    font = ImageFont.truetype(font=ICONS_FONT_FILE_PATH, size=font_size)
    image = Image.new(mode="RGBA", size=(width, height), color=(255, 255, 255, 0))

    new_data = []
    for _ in image.getdata():
        new_data.append((255, 255, 255, 0))

    image.putdata(new_data)

    draw = ImageDraw.Draw(im=image)
    draw.text(xy=(width / 2, height / 2), text=symbol, font=font, fill=color, anchor='mm')

    photo_image = PhotoImage(data=image_to_byte_array(image))
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
