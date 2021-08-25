from itertools import chain
from operator import itemgetter


def parse(data1, data2, file_type='json'):
    def get_line(sign, key, value):
        return '  {} {}: {}'.format(sign, key, value)

    def convert_value(value):
        if value is None:
            return 'null'
        return str(value).lower()

    def difference(dict1, dict2, sign):
        return ((key, get_line(sign, key, convert_value(dict1.get(key))))
                for key in dict1.keys() - dict2.keys())

    only_from_data1 = difference(data1, data2, '-')
    only_from_data2 = difference(data2, data1, '+')
    common_keys = data1.keys() & data2.keys()
    equal_values = ((key, get_line(' ', key, convert_value(data2.get(key))))
                    for key in filter(lambda k: data1.get(k) == data2.get(k),
                                      common_keys))
    different_values = ((key, '\n'.join(
        [get_line('-', key, convert_value(data1.get(key))),
         get_line('+', key, convert_value(data2.get(key))),
         ])) for key in filter(lambda k: data1.get(k) != data2.get(k),
                               common_keys))
    result = ['{']
    result.extend(map(itemgetter(1),
                      sorted(chain(only_from_data1,
                                   only_from_data2,
                                   equal_values,
                                   different_values))))
    result.append('}')

    print(result)
    return '\n'.join(result)
