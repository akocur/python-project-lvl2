import json

import yaml

from gendiff.formats import get_formatter
from gendiff.parse import parse


def generate_diff(file_path1, file_path2, format_name='stylish'):
    """
    Generate diff between file_path1 and file_path2 files.

    Return result in format_name format.
    The available formats are described in the get_formatter function from
    gendiff.formats.

    :param file_path1: str
    :param file_path2: str
    :param format_name: str
    :return: str
    """
    data1 = _load(file_path1)
    data2 = _load(file_path2)
    format_ = get_formatter(format_name)
    return format_(parse(data1, data2))


def _load(file_path):
    if _file_type(file_path) == 'yaml':
        return yaml.safe_load(open(file_path))
    return json.load(open(file_path))


def _file_type(file_path):
    if file_path.endswith(('.yaml', '.yml')):
        return 'yaml'
    if file_path.endswith('.json'):
        return 'json'
    return None
