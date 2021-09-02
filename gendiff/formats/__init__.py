from gendiff.formats.plain import plain
from gendiff.formats.stylish import stylish
from gendiff.formats.json import formatted_to_json

FORMAT_PLAIN = 'plain'
FORMAT_JSON = 'json'
FORMAT_STYLISH = 'stylish'


def get_formatter(format_name):
    """
    Return formatter by format_name.

    :param format_name: str
        one of the available formatters.
    :return: formatting function
    """
    return {
        FORMAT_STYLISH: stylish,
        FORMAT_PLAIN: plain,
        FORMAT_JSON: formatted_to_json,
    }.get(format_name)


def get_default_format_name():
    """Return default format name."""
    return FORMAT_STYLISH


def get_available_formatters():
    """Return available formatters."""
    return [FORMAT_STYLISH, FORMAT_PLAIN, FORMAT_JSON]
