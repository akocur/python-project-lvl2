from itertools import chain
from operator import itemgetter
import json
import yaml


def parse(data1, data2, file_type='json'):
    def get_line(sign, key, value):
        return '  {} {}: {}'.format(sign, key, value)

    def convert_value(value):
        if isinstance(value, str):
            return value
        if file_type == 'json':
            return json.dumps(value)
        return yaml.safe_dump(value)[:-5]

    def difference(dict1, dict2, sign):
        return ((key, get_line(sign, key, convert_value(dict1.get(key))))
                for key in dict1.keys() - dict2.keys())

    only_data1 = difference(data1, data2, '-')
    only_data2 = difference(data2, data1, '+')
    key_intersection = data1.keys() & data2.keys()
    equal_values = ((key, get_line(' ', key, convert_value(data2.get(key))))
                    for key in filter(lambda k: data1.get(k) == data2.get(k),
                                      key_intersection))
    different_values = ((key, '\n'.join(
        [get_line('-', key, convert_value(data1.get(key))),
         get_line('+', key, convert_value(data2.get(key))),
         ])) for key in filter(lambda k: data1.get(k) != data2.get(k),
                               key_intersection))
    result = ['{']
    result.extend(map(itemgetter(1),
                      sorted(chain(only_data1,
                                   only_data2,
                                   equal_values,
                                   different_values))))
    result.append('}')

    print(result)
    return '\n'.join(result)
