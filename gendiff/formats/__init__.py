import gendiff.formats.plain
import gendiff.formats.stylish
import gendiff.formats.json

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
    if format_name == FORMAT_PLAIN:
        return gendiff.formats.plain.plain
    if format_name == FORMAT_JSON:
        return gendiff.formats.json.formatted_to_json
    return get_default_formatter()


def get_default_formatter():
    """Return default formatter."""
    return gendiff.formats.stylish.stylish


def get_available_formatters():
    """Return available formatters."""
    return [FORMAT_STYLISH, FORMAT_PLAIN, FORMAT_JSON]
