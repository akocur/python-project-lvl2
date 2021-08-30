from itertools import chain


STATUS_NEW = 'new'
STATUS_DELETE = 'delete'
STATUS_EQUAL = 'equal'
STATUS_MODIFY = 'modify'


def evaluate_status(key1, value1, key2, value2):
    if key1 is None:
        return STATUS_NEW
    if key2 is None:
        return STATUS_DELETE
    if isinstance(value1, dict) and isinstance(value2, dict):
        return None
    if value1 == value2:
        return STATUS_EQUAL
    return STATUS_MODIFY


def make_diff(key1, value1, key2, value2):
    children = None
    if isinstance(value1, dict) and isinstance(value2, dict):
        children = list(map(
            lambda x: make_diff(*x), get_keys_values(value1, value2)
        ))

    return {
        'key': key1 if key2 is None else key2,
        'status': evaluate_status(key1, value1, key2, value2),
        'old_value': value1,
        'new_value': value2,
        'children': children,
    }


def get_key(diff):
    return diff['key']


def get_status(diff):
    return diff['status']


def get_old_value(diff):
    return diff['old_value']


def get_new_value(diff):
    return diff['new_value']


def get_children(diff):
    return diff['children']


def get_keys_values(dict1, dict2):

    keys1 = dict1.keys()
    keys2 = dict2.keys()
    only_dict1 = ((key, dict1[key], None, None) for key in keys1 - keys2)
    only_dict2 = ((None, None, key, dict2[key]) for key in keys2 - keys1)
    equal = ((key, dict1[key], key, dict2[key]) for key in keys1 & keys2)

    return chain(only_dict1, only_dict2, equal)
