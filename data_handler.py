import json
import os

def save_group(group, filename="group_data.json"):
    data = group.to_dict()
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f" Saved!")

def load_group(filename="group_data.json"):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        data = json.load(f)
    from group import Group
    return Group.from_dict(data)