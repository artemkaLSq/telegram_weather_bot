from PIL import Image, ImageDraw
from datetime import datetime
import requests


class PictureCreator:

    @staticmethod
    def create_pic(url, state, value, unit):
        img = Image.new('RGB', (256, 256), (0, 0, 255))
        img_w, img_h = img.size
        weather_icon = Image.open(requests.get(url, stream=True).raw)
        wth_w, wth_h = weather_icon.size
        offset = ((img_w - wth_w) // 2, (img_h - wth_h) // 2)
        img.paste(weather_icon, offset)
        d = ImageDraw.Draw(img)
        d.text((15, 15), f"{value} {unit}", anchor="ms", fill=(255, 255, 0))
        filename = 'image.png'
        img.save(filename)
        return filename
