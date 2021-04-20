import json
import os
from json.decoder import JSONDecodeError
from typing import List, Dict, Any


class DataStoreService:
    __root = "data"

    @classmethod
    def get_by(cls, field_name: str, value: Any,  _filename: str) -> List[Dict]:
        return [row for row in cls.load(_filename) if row.get(field_name) == value]

    @classmethod
    def load(cls, _filename: str) -> List[Dict]:
        try:
            with open(os.path.join(cls.__root, _filename), "r") as fl:
                return json.loads(fl.read())
        except IOError as _:
            return []
        except JSONDecodeError as _:
            return []

    @classmethod
    def save(cls, _data: Dict, _filename: str) -> None:
        _rows = list(filter(lambda x: _data.get("id", None) != x.get("id", None), cls.load(_filename)))
        _rows.append(_data)
        cls._file_refresh(_rows, _filename)

    @classmethod
    def save_all(cls, _rows: List[Dict], _filename: str) -> None:
        _items = []
        _ids = set(map(lambda x: x.get("id"), _rows))
        for _raw_data in cls.load(_filename):
            _status = _raw_data.get("id") in _ids
            if not _status:
                _items.append(_raw_data)
        _items.extend(_rows)
        cls._file_refresh(_items, _filename)

    @classmethod
    def remove(cls, _id: str, _filename: str) -> None:
        _rows = list(filter(lambda x: _id != x.get("id", None), cls.load(_filename)))
        cls._file_refresh(_rows, _filename)

    @classmethod
    def remove_children(cls, _pid: str, _filename: str) -> None:
        _rows = list(filter(lambda x: _pid != x.get("pid", None), cls.load(_filename)))
        cls._file_refresh(_rows, _filename)

    @classmethod
    def _file_refresh(cls, _rows: List[Dict], _filename: str) -> None:
        try:
            with open(os.path.join(cls.__root, _filename), "w") as fl:
                json.dump(_rows, fl)
        finally:
            pass

    @classmethod
    def create(cls, _rows: List[Dict], _filename: str) -> None:
        cls._file_refresh(_rows, _filename)