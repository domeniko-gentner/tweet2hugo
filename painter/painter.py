#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /**********************************************************************************
#  * _author  : Domeniko Gentner
#  * _mail    : code@tuxstash.de
#  * _repo    : https://git.tuxstash.de/gothseidank/tweet2png
#  * _license : This project is under MIT License
#  *********************************************************************************/
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from json import load as j_load


class painter:

    def __init__(self, twitter: str, handle: str):
        # Load json
        css = Path("css.json")
        with css.open('r') as fp:
            css = j_load(fp)

        # Size
        img_size = (css['dimensions']['x'], css['dimensions']['y'])

        # Background color
        background_color = (css["background"]['r'], css["background"]['g'], css["background"]['b'])

        # text options
        text = css['text']
        color = (text['color']['r'], text['color']['g'], text['color']['b'])
        font = text['font']
        size = text['size']

        image = Image.new('RGB', img_size, background_color)
        font = ImageFont.truetype(font)

        context = ImageDraw.Draw(image)
        context.text((10, 10), handle, fill=color, font=font)

        image.save('test.png')
