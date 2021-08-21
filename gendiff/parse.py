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

    keys1 = data1.keys()
    keys2 = data2.keys()
    only_data1 = ((key, get_line('-', key, convert_value(data1.get(key))))
                  for key in keys1 - keys2)
    only_data2 = ((key, get_line('+', key, convert_value(data2.get(key))))
                  for key in keys2 - keys1)
    equal_values = ((key, get_line(' ', key, convert_value(data2.get(key))))
                    for key in filter(lambda k: data1.get(k) == data2.get(k),
                                      keys1 & keys2))
    different_values = ((key, '\n'.join(
        [get_line('-', key, convert_value(data1.get(key))),
         get_line('+', key, convert_value(data2.get(key))),
         ])) for key in filter(lambda k: data1.get(k) != data2.get(k),
                               keys1 & keys2))
    result = ['{']
    result.extend(map(itemgetter(1),
                      sorted(chain(only_data1,
                                   only_data2,
                                   equal_values,
                                   different_values))))
    result.append('}')

    print(result)
    return '\n'.join(result)
