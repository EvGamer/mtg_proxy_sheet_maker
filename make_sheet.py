import json
import sys
import os
from math import floor
from itertools import repeat, groupby
from pathlib import Path
from units import to_pixels

from PIL import Image, ImageOps


def repeated_files(files):
    for file in files:

        yield from repeat(file, file['quantity'])

def files(settings):
    files = settings['files']

    for file_settings in files:
        path = Path(settings['dir']) / file_settings['file_name']
        with Image.open(path) as image:
            yield {**file_settings, 'image': image}


def deenumerate(enumerated):
    for i, item in enumerated:
        yield item


def batches(files, amount):
    group = lambda item: floor(item[0] / amount)

    for _, page in groupby(enumerate(files), group):
        yield deenumerate(page)

def make_sheet(path_arg):
    path = Path(path_arg)

    with open(path/'settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    try:
        os.mkdir(path/'output')
    except FileExistsError:
        pass

    dpi = settings['dpi']
    card_height = to_pixels(settings['height'], dpi)
    card_width = to_pixels(settings['width'], dpi)
    gap_x = to_pixels(settings['gaps']['x'], dpi)
    gap_y = to_pixels(settings['gaps']['y'], dpi)

    rows_count = 3
    columns_count = 3

    sheet_width = card_width * columns_count + gap_x * (columns_count - 1)
    sheet_height = card_height * rows_count + gap_y * (rows_count - 1)

    print(card_height, card_width, gap_x, gap_y)

    for page in batches(batches(repeated_files(files(settings)), rows_count), columns_count):
        sheet = Image.new('RGBA', (sheet_width, sheet_height))
        for row_num, row in enumerate(page):
            for col_num, file in enumerate(row):
                print(row_num, col_num, file)




if __name__ == '__main__':
    path_arg = sys.argv[1]

    make_sheet(path_arg)

