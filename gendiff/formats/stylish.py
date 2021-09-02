from itertools import starmap

import gendiff.diff as diff

sign_added = '+'
sign_deleted = '-'
sign_unchanged = ' '
char_for_indent = ' '
indent_width = 2
width_between_sign_and_key = 1 + max(map(
    len, (sign_added, sign_deleted, sign_unchanged)
))


def _formatted_value(value, current_indent_width):
    if value is None:
        return 'null'
    if value in (False, True):
        return str(value).lower()
    if isinstance(value, dict):
        result = ['{']
        indent = char_for_indent * current_indent_width
        lines = starmap(
            lambda key, val: _make_line(
                indent,
                ' ',
                key,
                _formatted_value(val, _new_indent_width(current_indent_width))
            ),
            value.items()
        )
        result.extend(lines)
        result.append(_make_end_bracket(current_indent_width))
        return '\n'.join(result)
    return value


def _get_line(current_diff, current_indent_width):
    """Return a line, depending on the diff status."""
    indent = char_for_indent * current_indent_width
    status = diff.get_status(current_diff)
    key = diff.get_key(current_diff)
    old_value = diff.get_old_value(current_diff)
    new_value = diff.get_new_value(current_diff)
    if status is None:
        children = diff.get_children(current_diff)
        line = _make_line(
            indent,
            sign_unchanged,
            key,
            stylish(children, _new_indent_width(current_indent_width))
        )
    elif status == diff.STATUS_MODIFIED:
        line1 = _make_line(
            indent,
            sign_deleted,
            key,
            _formatted_value(
                old_value,
                _new_indent_width(current_indent_width)
            )
        )
        line2 = _make_line(
            indent,
            sign_added,
            key,
            _formatted_value(
                new_value,
                _new_indent_width(current_indent_width)
            )
        )
        line = '\n'.join([line1, line2])
    elif status == diff.STATUS_ADDED:
        line = _make_line(
            indent,
            sign_added,
            key,
            _formatted_value(
                new_value,
                _new_indent_width(current_indent_width)
            )
        )
    elif status == diff.STATUS_DELETED:
        line = _make_line(
            indent,
            sign_deleted,
            key,
            _formatted_value(
                old_value,
                _new_indent_width(current_indent_width)
            )
        )
    else:
        line = _make_line(
            indent,
            sign_unchanged,
            key,
            _formatted_value(
                old_value,
                _new_indent_width(current_indent_width)
            )
        )
    return line


def _make_end_bracket(current_indent_width):
    """Return } with the necessary indentation."""
    prev_indent_width = current_indent_width - width_between_sign_and_key
    indent = char_for_indent * prev_indent_width
    end_bracket = '{}{}'.format(indent, '}')
    return end_bracket


def _make_line(indent, sign, key, value):
    return '{}{} {}: {}'.format(indent, sign, key, value)


def _new_indent_width(current_indent_width):
    return current_indent_width + indent_width + width_between_sign_and_key


def stylish(diffs, current_indent_width=indent_width):
    """
    Format the diff list to stylish format.

    + is if status of diff is added.
    - is if status of diff is deleted.
    if status of diff is modified, then first add line with old value with
    sign -, second add new value with sign +.
    if diff has children, then no sign.

    Example:
    {
        common: {
          + follow: false
            setting1: Value 1
          - setting2: 200
          - setting3: true
          + setting3: null
          + setting4: blah blah
          + setting5: {
                key5: value5
            }
            setting6: {
                doge: {
                  - wow:
                  + wow: so much
                }
                key: value
              + ops: vops
            }
        }
      - group2: {
            abc: 12345
            deep: {
                id: 45
            }
        }
    }

    :param diffs: list of diff
        See make_diff from gendiff.diff package.
    :param current_indent_width: int
    :return:
    """
    lines = ['{']
    new_lines = map(
        lambda current_diff: _get_line(current_diff, current_indent_width),
        sorted(diffs, key=diff.get_key),
    )
    lines.extend(new_lines)
    lines.append(_make_end_bracket(current_indent_width))
    return '\n'.join(lines)
