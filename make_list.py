import json
import sys
from pathlib import Path


def filter_images(paths):
    for path in paths:
        if str(path).split('.')[1] in ('png', 'jpg'):
            yield path


def make_list(path_arg):
    path = Path(path_arg)

    settings = {
        'height': 2.5,
        'width': 3.5,
        'dpi': 298,
        'gaps': {
            'x': 10,
            'y': 10,
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

