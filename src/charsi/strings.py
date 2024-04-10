from __future__ import annotations
import json
from enum import Enum
from typing import List, Dict, TypedDict, IO


# pylint: disable=invalid-name
class LanguageTag(Enum):
    enUS = 'enUS'
    zhTW = 'zhTW'
    deDE = 'deDE'
    esES = 'esES'
    frFR = 'frFR'
    itIT = 'itIT'
    koKR = 'koKR'
    plPL = 'plPL'
    esMX = 'esMX'
    jaJP = 'jaJP'
    ptBR = 'ptBR'
    ruRU = 'ruRU'
    zhCN = 'zhCN'

    @staticmethod
    def tags() -> List[str]:
        return [tag.value for tag in LanguageTag]


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

    def dump(self, fp: IO):
        json.dump(self.items, fp, ensure_ascii=False, indent=2)
