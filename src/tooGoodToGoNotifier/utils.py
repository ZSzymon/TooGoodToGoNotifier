import json


def saveToJson(items, filepath):
    with open(filepath, 'w') as f:
        f.write(json.dumps(items, indent=4))


def readToJson(path):
    with open(path, "r") as f:
        credentials = f.read()
        return json.loads(credentials)


def print_list(active):
    if not active:
        print("Empty ")
    for item in active:
        item = str(item).replace("'", '"')
        item = json.dumps(item)
        print(item)


