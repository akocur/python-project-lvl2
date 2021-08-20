import json
from operator import itemgetter
from itertools import chain


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
    only_json1 = ((key, get_line('-', key, value_to_json(json1.get(key))))
                  for key in keys1 - keys2)
    only_json2 = ((key, get_line('+', key, value_to_json(json2.get(key))))
                  for key in keys2 - keys1)
    equal_values = ((key, get_line(' ', key, value_to_json(json2.get(key))))
                    for key in filter(lambda k: json1.get(k) == json2.get(k),
                                      keys1 & keys2))
    different_values = ((key, '\n'.join(
        [get_line('-', key, value_to_json(json1.get(key))),
         get_line('+', key, value_to_json(json2.get(key))),
         ]))
        for key in filter(lambda k: json1.get(k) != json2.get(k),
                          keys1 & keys2))
    result = ['{']
    result.extend(map(itemgetter(1),
                      sorted(chain(only_json1,
                                   only_json2,
                                   equal_values,
                                   different_values))))
    result.append('}')
    print(result)
    return '\n'.join(result)
