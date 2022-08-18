import json
from typing import Any, Dict

from pysondb import db
from pysondb.db import JsonDatabase
from pysondb.errors import IdNotFoundError


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


class JsonDb(JsonDatabase):

    def __init__(self, filename: str):
        super().__init__(filename)
        self.db_path = filename
        self.connection: JsonDatabase = self.connect_to_db()

    def connect_to_db(self):
        connection = db.getDb(self.db_path)
        return connection

    def exist(self, pk):
        _exist = self.getByQuery({"_my_id": pk})
        return len(_exist) > 0

    def add(self, pk, new_data: Dict[str, Any]) -> int:
        super().add({"_my_id": pk, "obj": new_data})

    def addIfUnique(self, pk, obj):
        if self.exist(pk):
            return False
        else:
            self.add(pk, obj)
            return True

    def addManyIfUnique(self, objects, pks):
        assert len(objects) == len(pks)
        for pks, obj in zip(pks, objects):
            self.addIfUnique(pks, obj)
