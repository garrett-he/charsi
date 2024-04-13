from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional

from .utils import split_text


def parse(text: str) -> Instruction:
    fds = split_text(split_text(text, '#')[0], ':')
    if len(fds) < 2:
        raise InstructionFormatError(text)

    m = re.match(r'^\s*(\w+)\s*(\[[^]]+])\s*(\[[^]]+])?', fds[0])

    if not m:
        raise InstructionFormatError(text)

    return Instruction(
        name=m.group(1),
        query=m.group(2).strip(' []'),
        args=[arg.strip() for arg in fds[1].split(',')],
        lang=None if m.group(3) is None else m.group(3).strip(' []')
    )


@dataclass
class Instruction:
    name: str
    query: str
    args: List[str]
    lang: Optional[str] = None


class InstructionInvoker:
    _handlers: Dict[str, Callable]

    default: InstructionInvoker

    def __init__(self):
        self._handlers = {}

    def register(self, name: str, handler: Callable):
        if name in self._handlers:
            raise InstructionConflictError(name)

        self._handlers[name] = handler

    def unregister(self, name: str):
        if name not in self._handlers:
            raise InstructionUndefinedError(name)

        del self._handlers[name]

    def is_registered(self, name: str):
        return name in self._handlers

    def invoke(self, inst: Instruction, text: str) -> str:
        if not self.is_registered(inst.name):
            raise InstructionUndefinedError(inst.name)

        return self._handlers[inst.name](text, *inst.args)


class _InstructionError(Exception):
    ...


class InstructionFormatError(_InstructionError):
    ...


class InstructionConflictError(_InstructionError):
    ...


class InstructionUndefinedError(_InstructionError):
    ...


def replace_text_handler(_, *args):
    return args[0].replace('\\n', '\n')


InstructionInvoker.default = InstructionInvoker()
InstructionInvoker.default.register('Text', replace_text_handler)
