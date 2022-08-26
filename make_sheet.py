import json
import sys
import os
from math import floor
from itertools import repeat, groupby
from pathlib import Path
from units import to_pixels

from PIL import Image, ImageOps, ImageChops


def repeated(files):
    for file in files:

        yield from repeat(file, file['quantity'])


def files(settings):
    files = settings['files']

    for file_settings in files:
        path = Path(settings['dir']) / file_settings['file_name']
        with Image.open(path) as image:
            yield {**file_settings, 'image': image.convert('RGBA')}


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


    output_path = path/'output'

    try:
        os.mkdir(output_path)
    except FileExistsError:
        pass


    dpi = settings['dpi']
    card_height = to_pixels(settings['height'], dpi)
    card_width = to_pixels(settings['width'], dpi)
    gap_x = to_pixels(settings['gaps']['x'], dpi)
    gap_y = to_pixels(settings['gaps']['y'], dpi)

    rows_count = 3
    columns_count = 3

    def get_offset_x(card_count):
        return (card_width + gap_x) * card_count

    def get_offset_y(card_count):
        return (card_height + gap_y) * card_count

    def get_width(card_count):
        return card_width + get_offset_x(card_count - 1)

    def get_height(card_count):
        return card_height + get_offset_y(card_count - 1)

    def get_size(_columns_count, _rows_count):
        return get_width(_columns_count), get_height(_rows_count)

    def rows(_files):
        return batches(_files, columns_count)

    def pages(_files):
        return batches(rows(_files), rows_count)

    for page_num, page in enumerate(pages(repeated(files(settings)))):
        sheet_size = get_size(rows_count, columns_count)
        sheet = Image.new('RGBA', sheet_size)
        for row_num, row in enumerate(page):
            for col_num, file in enumerate(row):
                image = file['image']

                sheet.paste(image, (get_offset_x(col_num), get_offset_y(row_num)))

        sheet.save(output_path/f'sheet_{page_num}.png')


if __name__ == '__main__':
    path_arg = sys.argv[1]

    make_sheet(path_arg)

