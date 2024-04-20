import re
from typing import List, Dict, IO
from .instruction import parse, Instruction, InstructionInvoker
from .utils import filter_irrelevant_lines, split_text
from .strings import StringTable, LanguageTag


class Recipe:
    instructions: List[Instruction]
    tags: Dict[str, str]
    _var_tables: dict

    def read(self, fp: IO):
        lines = [line.strip() for line in fp.readlines()]
        self.instructions = [parse(line) for line in filter_irrelevant_lines(lines)]
        self.tags = {}
        self._var_tables = {}

        for line in filter(lambda line: line != '' and line[0:2] == '##', lines):
            fds = split_text(line, ':')
            self.tags[fds[0][2:].strip()] = fds[1].strip()

        return self

    def build(self, tbl: StringTable, invoker: InstructionInvoker = InstructionInvoker.default):
        def update_vars(key: str, text: str):
            m = re.findall(r'({[\w-]+})', text)

            if not m:
                return text

            for name in map(lambda v: v.strip('{}'), m):
                if name not in self._var_tables or key not in self._var_tables[name]:
                    var = ''
                else:
                    var = self._var_tables[name][key]

                text = text.replace('{%s}' % name, var)

            return text.strip()

        for inst in self.instructions:
            if (inst.lang is None) and ('Language' in self.tags):
                inst.lang = self.tags['Language']

            langs = LanguageTag.tags() if inst.lang is None else [inst.lang]

            for s in tbl.findall(inst.query):
                s.update({lang: update_vars(s['Key'], invoker.invoke(inst, s[lang])) for lang in langs})

    def set_var_table(self, key: str, var_table: dict):
        self._var_tables[key] = var_table
