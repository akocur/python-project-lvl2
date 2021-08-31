import gendiff.formats.plain
import gendiff.formats.stylish


def get_formatter(format_name):
    if format_name == 'plain':
        return gendiff.formats.plain.plain
    return gendiff.formats.stylish.stylish
