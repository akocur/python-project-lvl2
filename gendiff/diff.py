from itertools import chain


STATUS_ADDED = 'added'
STATUS_DELETED = 'deleted'
STATUS_UNCHANGED = 'unchanged'
STATUS_MODIFIED = 'modified'


def _evaluate_status(key1, value1, key2, value2):
    status = STATUS_MODIFIED
    if key1 is None:
        status = STATUS_ADDED
    if key2 is None:
        status = STATUS_DELETED
    if isinstance(value1, dict) and isinstance(value2, dict):
        status = None
    if value1 == value2:
        status = STATUS_UNCHANGED
    return status


def get_children(diff):
    """Return children of diff.

    :param diff: value returned by make_diff function
    :return: children of diff
    """
    return diff['children']


def get_key(diff):
    """
    Return key of diff.

    :param diff: value returned by make_diff function
    :return: key of diff
    """
    return diff['key']


def get_keys_values(dict1, dict2):
    """
    Make an iterator that returns tuple (key1, value1, key2, value2).

    key1, value1 from dict1. key2, value2 from dict2.
    If key1 or key2 or value1 or value2 does not exist, then None is
    substituted instead.

    :param dict1: dict
    :param dict2: dict
    :return: iterator of tuple (key1, value1, key2, value2)
    """
    keys1 = dict1.keys()
    keys2 = dict2.keys()
    only_from_dict1 = ((key, dict1[key], None, None) for key in keys1 - keys2)
    only_from_dict2 = ((None, None, key, dict2[key]) for key in keys2 - keys1)
    equal = ((key, dict1[key], key, dict2[key]) for key in keys1 & keys2)

    return chain(only_from_dict1, only_from_dict2, equal)


def get_new_value(diff):
    """
    Return new_value from diff.

    :param diff: value returned by make_diff function
    :return: new_value of diff
    """
    return diff['new_value']


def get_old_value(diff):
    """
    Return old_value from diff.

    :param diff: value returned by make_diff function
    :return: old_value of diff
    """
    return diff['old_value']


def get_status(diff):
    """
    Return status from diff.

    :param diff: value returned by make_diff function
    :return: status of diff
    """
    return diff['status']


def make_diff(key1, value1, key2, value2):
    """
    Make diff abstraction.

    diff appears as a result of comparing two keys from the compared
    dictionaries. diff is a dictionary with the keys: key, status, old_value,
    new_value, children, where:
        key - key1 if key2 is None else key2.
        status - any from:
                'added' if key2 was added to dict2;
                'deleted' if key1 was deleted from dict2;
                'unchanged' if values is equal for key1 and key2;
                'modified' if values is different for key1 and key2.
        old_value - value for key1, that is, value1.
        new_value - value for key2, that is, value2.
        children - list of diff if key1 == key2, value1 and value2 are dict.

    :param key1: any hashable value or None
    :param value1: any
    :param key2: any hashable value or None
    :param value2: any
    :return: dict
    """
    children = None
    if isinstance(value1, dict) and isinstance(value2, dict):
        children = list(map(
            lambda x: make_diff(*x), get_keys_values(value1, value2)
        ))

    return {
        'key': key1 if key2 is None else key2,
        'status': _evaluate_status(key1, value1, key2, value2),
        'old_value': value1,
        'new_value': value2,
        'children': children,
    }
