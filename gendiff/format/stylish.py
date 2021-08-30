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


def format_(value, current_indent_width):
    if value is None:
        return 'null'
    if value in (False, True):
        return str(value).lower()
    if isinstance(value, dict):
        result = ['{']
        indent = char_for_indent * current_indent_width
        lines = starmap(
            lambda key, val: make_line(
                indent,
                ' ',
                key,
                format_(val, new_indent_width(current_indent_width))
            ),
            value.items()
        )
        result.extend(lines)
        result.append(make_end_bracket(current_indent_width))
        return '\n'.join(result)
    return value


def make_end_bracket(current_indent_width):
    prev_indent_width = current_indent_width - width_between_sign_and_key
    indent = char_for_indent * prev_indent_width
    end_bracket = '{}{}'.format(indent, '}')
    return end_bracket


def make_line(indent, sign, key, value):
    return '{}{} {}:{}{}'.format(indent,
                                 sign,
                                 key,
                                 ' ' if value else '',
                                 value)


def new_indent_width(current_indent_width):
    return current_indent_width + indent_width + width_between_sign_and_key


def get_line(current_diff, current_indent_width):
    indent = char_for_indent * current_indent_width
    status = diff.get_status(current_diff)
    key = diff.get_key(current_diff)
    old_value = diff.get_old_value(current_diff)
    new_value = diff.get_new_value(current_diff)
    if status is None:
        children = diff.get_children(current_diff)
        line = make_line(
            indent,
            sign_unchanged,
            key,
            stylish(children, new_indent_width(current_indent_width))
        )
    elif status == diff.STATUS_MODIFIED:
        line1 = make_line(
            indent,
            sign_deleted,
            key,
            format_(old_value, new_indent_width(current_indent_width)))
        line2 = make_line(
            indent,
            sign_added,
            key,
            format_(new_value, new_indent_width(current_indent_width)))
        line = '\n'.join([line1, line2])
    elif status == diff.STATUS_ADDED:
        line = make_line(
            indent,
            sign_added,
            key,
            format_(new_value, new_indent_width(current_indent_width))
        )
    elif status == diff.STATUS_DELETED:
        line = make_line(
            indent,
            sign_deleted,
            key,
            format_(old_value, new_indent_width(current_indent_width))
        )
    else:
        line = make_line(
            indent,
            sign_unchanged,
            key,
            format_(old_value, new_indent_width(current_indent_width))
        )
    return line


def stylish(diffs, current_indent_width=indent_width):
    lines = ['{']
    new_lines = map(
        lambda current_diff: get_line(current_diff, current_indent_width),
        sorted(diffs, key=diff.get_key),
    )
    lines.extend(new_lines)
    lines.append(make_end_bracket(current_indent_width))
    return '\n'.join(lines)
