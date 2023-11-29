import json


def get_json(dname: str) -> dict:
    with open(dname, 'r', encoding='UTF-8') as f:
        data = json.load(f)
    return data
