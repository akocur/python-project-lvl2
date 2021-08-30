from gendiff.diff import make_diff
from gendiff.diff import get_keys_values


def parse(data1, data2):
    """
    Return list diffs.
    :param data1: dict
    :param data2: dict
    :return: list of diffs
    """
    diffs = list(map(lambda x: make_diff(*x), get_keys_values(data1, data2)))
    return diffs
