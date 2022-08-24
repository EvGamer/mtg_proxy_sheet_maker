import json
import sys
import os
from math import floor
from itertools import repeat, groupby
from pathlib import Path


def repeated_files(files):
    for file in files:
        yield from repeat(file, file['quantity'])


def pages(files, amount):
    page_grouping = lambda item: floor(item[0] / amount)

    for page in groupby(enumerate(files), page_grouping):
        yield from (item[1] for item in page[1])


def make_sheet(path_arg):
    path = Path(path_arg)

    with open(path/'settings.json', 'r') as settings_file:
        settings = json.load(settings_file)

    try:
        os.mkdir(path/'output')
    except FileExistsError:
        pass

    print(list(pages(repeated_files(settings['files']), 9)))


if __name__ == '__main__':
    path_arg = sys.argv[1]

    make_sheet(path_arg)

