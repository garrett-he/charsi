from typing import List, Dict, IO
from .instruction import parse, Instruction, InstructionInvoker
from .utils import filter_irrelevant_lines
from .strings import StringTable, LanguageTag


class Recipe:
    instructions: List[Instruction]
    tags: Dict[str, str]

    def read(self, fp: IO):
        self.instructions = [parse(line) for line in filter_irrelevant_lines(fp.readlines())]

        return self

    def build(self, tbl: StringTable, invoker: InstructionInvoker = InstructionInvoker.default):
        for inst in self.instructions:
            langs = LanguageTag.tags() if inst.lang is None else [inst.lang]

            for s in tbl.findall(inst.query):
                s.update({lang: invoker.invoke(inst, s[lang]) for lang in langs})
