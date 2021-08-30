from gendiff.diff import get_keys_values


def test_get_keys_values():
    dict1 = {
        'k1': 'equal',
        'k2': None,
        'k3': 'delete',
    }
    dict2 = {
        'k1': 'equal',
        'k2': 'modify',
        'k4': 'new',
    }
    expect = [
        ('k1', 'equal', 'k1', 'equal'),
        ('k2', None, 'k2', 'modify'),
        ('k3', 'delete', None, None),
        (None, None, 'k4', 'new'),
    ]
    assert sorted(map(
        str, get_keys_values(dict1, dict2)
    )) == sorted(map(str, expect))
