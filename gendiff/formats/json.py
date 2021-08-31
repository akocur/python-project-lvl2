import json
from copy import deepcopy

import gendiff.diff as diff


def formatted_to_json(diffs):

    def sort_children(current_diff):
        children = diff.get_children(current_diff)
        if children:
            children.sort(key=diff.get_key)
            list(map(sort_children, children))

    copy_diffs = sorted(deepcopy(diffs), key=diff.get_key)
    list(map(sort_children, copy_diffs))

    return json.dumps(copy_diffs, indent=2)
