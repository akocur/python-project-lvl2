import json


def generate_diff(file_path1, file_path2):
    def get_line(sign, key, value):
        return '  {} {}: {}'.format(sign, key, value)

    def value_to_json(value):
        if isinstance(value, str):
            return value
        return json.dumps(value)

    json1 = json.load(open(file_path1))
    json2 = json.load(open(file_path2))
    keys1 = json1.keys()
    keys2 = json2.keys()
    keys = sorted(list(keys1 | keys2))
    result = ['{']
    for key in keys:
        value1 = json1.get(key)
        value2 = json2.get(key)
        if key in keys1 and key not in keys2:
            line = get_line('-', key, value_to_json(value1))
            result.append(line)
        elif key in keys2 and key not in keys1:
            line = get_line('+', key, value_to_json(value2))
            result.append(line)
        elif value1 == value2:
            line = get_line(' ', key, value_to_json(value1))
            result.append(line)
        else:
            line1 = get_line('-', key, value_to_json(value1))
            line2 = get_line('+', key, value_to_json(value2))
            result.append(line1)
            result.append(line2)
    result.append('}')
    return '\n'.join(result)
