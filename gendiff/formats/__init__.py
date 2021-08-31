import gendiff.formats.plain
import gendiff.formats.stylish
import gendiff.formats.json


def get_formatter(format_name):
    if format_name == 'plain':
        return gendiff.formats.plain.plain
    if format_name == 'json':
        return gendiff.formats.json.formatted_to_json
    return gendiff.formats.stylish.stylish
