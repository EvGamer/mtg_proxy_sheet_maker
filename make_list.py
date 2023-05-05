import json
import sys
from pathlib import Path

from units import in_units, INCH, PIXEL


def filter_images(paths):
    for path in paths:
        split_path = str(path).split('.')
        if len(split_path) < 2:
            continue

        _, ext = split_path

        if ext not in ('png', 'jpg'):
            continue

        yield path


def make_list(path_arg):
    path = Path(path_arg)

    settings = {
        'height': in_units(3.5, INCH),
        'width': in_units(2.5, INCH),
        'dpi': 300,
        'gaps': {
            'x': in_units(10, PIXEL),
            'y': in_units(10, PIXEL),
        },
        'dir': str(path.absolute()),
        'files': []
    }

    for file_path in filter_images(path.iterdir()):
        settings['files'].append({
            'quantity': 1,
            'file_name': str(file_path.name),
        })

    with open(path/'settings.json', 'w') as settings_file:
        json.dump(settings, settings_file, indent=2)


if __name__ == '__main__':
    path_arg = sys.argv[1]

    make_list(path_arg)

