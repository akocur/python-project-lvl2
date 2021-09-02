import json
from copy import deepcopy

import gendiff.diff as diff


def formatted_to_json(diffs):
    """
    Format the diff list to json format.

    Output ordered by key from diff.

    Example:
    [
        {
            "key": "group3",
            "status": "added",
            "old_value": null,
            "new_value": {
              "deep": {
                "id": {
                  "number": 45
                }
              },
              "fee": 100500
            },
            "children": null
        }
    ]

    :param diffs: list of diff. See gendiff.diff package.
    :return: str
    """

    def sort_children(current_diff):
        children = diff.get_children(current_diff)
        if children:
            children.sort(key=diff.get_key)
            list(map(sort_children, children))

    copy_diffs = sorted(deepcopy(diffs), key=diff.get_key)
    list(map(sort_children, copy_diffs))

    return json.dumps(copy_diffs, indent=2)
