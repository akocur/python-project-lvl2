import json
import yaml
from gendiff.parse import parse
from gendiff.format.stylish import stylish


def generate_diff(file_path1, file_path2, format_=stylish):
    data1 = load(file_path1)
    data2 = load(file_path2)
    return format_(parse(data1, data2))


def load(file_path):
    if file_type(file_path) == 'yaml':
        return yaml.safe_load(open(file_path))
    return json.load(open(file_path))


def file_type(file_path):
    if file_path.endswith(('.yaml', '.yml')):
        return 'yaml'
    if file_path.endswith('.json'):
        return 'json'
    return None
