import gendiff.diff as diff


def flatten(lists):
    result = []

    def walk(node):
        for elem in node:
            if isinstance(elem, list):
                walk(elem)
            else:
                result.append(elem)

    walk(lists)
    return result


def formatted_value(value):
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


def make_added_line(key, value):
    return "Property '{}' was added with value: {}".format(
        key,
        formatted_value(value),
    )


def make_removed_line(key):
    return "Property '{}' was removed".format(key)


def make_updated_line(key, old_value, new_value):
    return "Property '{}' was updated. From {} to {}".format(
        key,
        formatted_value(old_value),
        formatted_value(new_value),
    )


def make_line(current_diff, keys):
    status = diff.get_status(current_diff)
    keys.append(diff.get_key(current_diff))
    if status is None:
        children = diff.get_children(current_diff)
        lines = make_lines(children, keys)
        keys.pop()
        return lines
    key = '.'.join(keys)
    new_value = diff.get_new_value(current_diff)
    line = ''
    if status == diff.STATUS_ADDED:
        line = make_added_line(key, new_value)
    elif status == diff.STATUS_DELETED:
        line = make_removed_line(key)
    elif status == diff.STATUS_MODIFIED:
        old_value = diff.get_old_value(current_diff)
        line = make_updated_line(key, old_value, new_value)
    keys.pop()
    return line


def make_lines(diffs, keys=None):
    if keys is None:
        keys = []
    changed_diffs = filter(
        lambda current_diff:
        (diff.get_status(current_diff) != diff.STATUS_UNCHANGED),
        diffs,
    )
    lines = list(map(
        lambda d: make_line(d, keys), sorted(changed_diffs, key=diff.get_key)
    ))
    return lines


def plain(diffs):
    lines = flatten(make_lines(diffs, []))
    return '\n'.join(lines)
