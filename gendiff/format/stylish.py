import gendiff.diff as diff


sign_new = '+'
sign_delete = '-'
sign_equal = ' '
char_for_indent = ' '
indent_width = 2
width_between_sign_and_key = 1 + max(map(
    len, (sign_new, sign_delete, sign_equal)
))


def make_line(indent, sign, key, value):
    return '{}{} {}:{}{}'.format(indent,
                                 sign,
                                 key,
                                 ' ' if value else '',
                                 value)


def make_end_bracket(current_indent_width):
    prev_indent_width = current_indent_width - width_between_sign_and_key
    indent = char_for_indent * prev_indent_width
    end_bracket = '{}{}'.format(indent, '}')
    return end_bracket


def new_indent_width(current_indent_width):
    return current_indent_width + indent_width + width_between_sign_and_key


def format_(value, current_indent_width):
    if value is None:
        return 'null'
    if value in (False, True):
        return str(value).lower()
    if isinstance(value, dict):
        result = ['{']
        indent = char_for_indent * current_indent_width
        for key, val in value.items():
            result.append(make_line(
                indent,
                ' ',
                key,
                format_(val, new_indent_width(current_indent_width)))
            )
        result.append(make_end_bracket(current_indent_width))
        return '\n'.join(result)
    return value


def stylish(diffs, current_indent_width=indent_width):
    lines = ['{']
    indent = char_for_indent * current_indent_width
    for current_diff in sorted(diffs, key=diff.get_key):
        status = diff.get_status(current_diff)
        key = diff.get_key(current_diff)
        old_value = diff.get_old_value(current_diff)
        new_value = diff.get_new_value(current_diff)
        if status is None:
            children = diff.get_children(current_diff)
            lines.append(
                make_line(
                    indent,
                    sign_equal,
                    key,
                    stylish(children, new_indent_width(current_indent_width))
                )
            )
        elif status == diff.STATUS_MODIFY:
            lines.append(make_line(
                indent,
                sign_delete,
                key,
                format_(old_value, new_indent_width(current_indent_width))
            ))
            lines.append(make_line(
                indent,
                sign_new,
                key,
                format_(new_value, new_indent_width(current_indent_width))
            ))
        elif status == diff.STATUS_NEW:
            lines.append(make_line(
                indent,
                sign_new,
                key,
                format_(new_value, new_indent_width(current_indent_width))
            ))
        elif status == diff.STATUS_DELETE:
            lines.append(make_line(
                indent,
                sign_delete,
                key,
                format_(old_value, new_indent_width(current_indent_width))
            ))
        else:
            lines.append(make_line(
                indent,
                sign_equal,
                key,
                format_(old_value, new_indent_width(current_indent_width))
            ))
    lines.append(make_end_bracket(current_indent_width))
    return '\n'.join(lines)
