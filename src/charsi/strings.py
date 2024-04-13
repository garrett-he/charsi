from __future__ import annotations
import json
import re
from enum import Enum
from functools import reduce
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

    def findall(self, query: str) -> List[dict]:
        if query.find(',') > -1:
            return reduce(lambda v, sl: v + sl, [self.findall(q.strip()) for q in query.split(',')], [])

        m = re.match(r'^\s*([\w\s]+)\s*~\s*([\w\s]+)\s*$', query)

        if not m:
            return [self.find(query)]

        if (m.group(1) not in self._item_indices) or (m.group(2) not in self._item_indices):
            raise IndexError(query)

        start_index = self._item_indices[m.group(1)]
        end_index = self._item_indices[m.group(2)] + 1
        if start_index > end_index:
            raise IndexError(query)

        return self.items[start_index:end_index]

    def dump(self, fp: IO):
        json.dump(self.items, fp, ensure_ascii=False, indent=2)
