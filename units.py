import math

INCH = 'inch'
PIXEL = 'px'
CENTIMETER = 'cm'


def in_units(value, unit):
    return {
        'value': value,
        'unit': unit,
    }


def to_pixels(value_unit, dpi):
    value = value_unit['value']
    unit = value_unit['unit']

    if unit == INCH:
        return math.floor(value * dpi)

    if unit == PIXEL:
        return value

    raise NotImplementedError(f'Conversion from {unit} is not implemented')
