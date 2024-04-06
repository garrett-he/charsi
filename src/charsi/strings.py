from __future__ import annotations
import json
from typing import List, Dict, TypedDict, IO


class StringItem(TypedDict):
    id: int
    Key: str
    enUS: str
    zhTW: str
    deDE: str
    esES: str
    frFR: str
    itIT: str
    koKR: str
    plPL: str
    esMX: str
    jaJP: str
    ptBR: str
    ruRU: str
    zhCN: str


class StringTable:
    items: List[StringItem]
    _item_indices: Dict[str, int]

    def __init__(self):
        self.items = []
        self._item_indices = {}

    def read(self, fp: IO) -> StringTable:
        self.items.clear()

        for item in json.load(fp):
            self.items.append(item)

        self._item_indices = {self.items[i]['Key']: i for i in range(0, len(self.items))}

        return self

    def write(self, fp: IO) -> StringTable:
        json.dump(self.items, fp, ensure_ascii=False, indent=2)

        return self

    def find(self, key: str) -> StringItem:
        if key not in self._item_indices:
            raise IndexError(key)

        return self.items[self._item_indices[key]]
