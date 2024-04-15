from typing import List, Dict, IO
from .instruction import parse, Instruction, InstructionInvoker
from .utils import filter_irrelevant_lines, split_text
from .strings import StringTable, LanguageTag


class Recipe:
    instructions: List[Instruction]
    tags: Dict[str, str]

    def read(self, fp: IO):
        lines = [line.strip() for line in fp.readlines()]
        self.instructions = [parse(line) for line in filter_irrelevant_lines(lines)]
        self.tags = {}

        for line in filter(lambda line: line != '' and line[0:2] == '##', lines):
            fds = split_text(line, ':')
            self.tags[fds[0][2:].strip()] = fds[1].strip()

        return self

    def build(self, tbl: StringTable, invoker: InstructionInvoker = InstructionInvoker.default):
        for inst in self.instructions:
            if (inst.lang is None) and ('Language' in self.tags):
                inst.lang = self.tags['Language']

            langs = LanguageTag.tags() if inst.lang is None else [inst.lang]

            for s in tbl.findall(inst.query):
                s.update({lang: invoker.invoke(inst, s[lang]) for lang in langs})
