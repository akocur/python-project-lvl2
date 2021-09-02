import gendiff.diff as diff


def _flatten(lists):
    """
    Flatten the list.

    Example:
    _flatten([1, [2, 3], [[5, 8], 9]]) == [1, 2, 3, 5, 8, 9]

    :param lists: list of list
    :return: list
    """
    def normalize(item):
        return _flatten(item) if isinstance(item, list) else [item]

    return sum(map(normalize, lists), [])


def _formatted_value(value):
    new_value = value
    if isinstance(value, dict):
        new_value = '[complex value]'
    elif value in (False, True):
        new_value = str(value).lower()
    elif value is None:
        new_value = 'null'
    elif isinstance(value, str):
        new_value = "'{}'".format(value)
    return new_value


def _make_added_line(key, value):
    return "Property '{}' was added with value: {}".format(
        key,
        _formatted_value(value),
    )


def _make_line(current_diff, keys):
    """
    Make one of the lines: added line, removed line, updated line.

    if diff has children, then return lines for the current_diff.
    keys is needed to create a path from keys for the current value.

    :param current_diff: diff
        See make_diff function from gendiff.diff package.
    :param keys: list of keys
    :return:
    """
    status = diff.get_status(current_diff)
    keys.append(diff.get_key(current_diff))
    if status is None:
        children = diff.get_children(current_diff)
        lines = _make_lines(children, keys)
        keys.pop()
        return lines
    key = '.'.join(keys)
    new_value = diff.get_new_value(current_diff)
    line = ''
    if status == diff.STATUS_ADDED:
        line = _make_added_line(key, new_value)
    elif status == diff.STATUS_DELETED:
        line = _make_removed_line(key)
    elif status == diff.STATUS_MODIFIED:
        old_value = diff.get_old_value(current_diff)
        line = _make_updated_line(key, old_value, new_value)
    keys.pop()
    return line


def _make_lines(diffs, parent_keys=None):
    """
    Make lines from diffs.

    parent_keys is list parent keys for current value.
    Lines order by key from diff.

    :param diffs: list if diff
        See make_diff function from gendiff.diff package
    :param parent_keys: list of keys
    :return:
    """
    if parent_keys is None:
        parent_keys = []
    changed_diffs = filter(
        lambda current_diff:
        (diff.get_status(current_diff) != diff.STATUS_UNCHANGED),
        diffs,
    )
    lines = list(map(
        lambda d: _make_line(d, parent_keys),
        sorted(changed_diffs, key=diff.get_key),
    ))
    return lines


def _make_removed_line(key):
    return "Property '{}' was removed".format(key)


def _make_updated_line(key, old_value, new_value):
    return "Property '{}' was updated. From {} to {}".format(
        key,
        _formatted_value(old_value),
        _formatted_value(new_value),
    )


def plain(diffs):
    """
    Format the diff list to plain format.

    Output ordered by key from diff. If the current diff has children, then
    a line will be created for each children, the property in which will
    consist of the parent keys.

    Example:
    Property 'common.follow' was added with value: false
    Property 'common.setting2' was removed
    Property 'common.setting3' was updated. From true to null
    Property 'common.setting5' was added with value: [complex value]
    Property 'key' was added with value: value

    :param diffs: list of diff. See gendiff.diff package.
    :return: str
    """
    lines = _flatten(_make_lines(diffs, []))
    return '\n'.join(lines)
