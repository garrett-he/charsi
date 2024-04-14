from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional

from lupa import LuaRuntime
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
    _lua: LuaRuntime

    default: InstructionInvoker

    def __init__(self):
        self._handlers = {}
        self._lua = LuaRuntime(unpack_returned_tuples=True, register_builtins=False)

        lua_globals = self._lua.globals()
        lua_globals['python'] = None
        lua_globals['RegisterInstruction'] = self.register
        lua_globals['UnregisterInstruction'] = self.unregister
        lua_globals['InstructionRegistered'] = self.is_registered

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

    def load_lua(self, codes: str):
        self._lua.execute(codes)


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


COLOR_CODES = {
    'WHITE': 'ÿc0',
    'RED': 'ÿc1',
    'LIGHTGREEN': 'ÿc2',
    'BLUE': 'ÿc3',
    'GOLD': 'ÿc4',
    'GRAY': 'ÿc5',
    'BLACK': 'ÿc6',
    'LIGHTGOLD': 'ÿc7',
    'ORANGE': 'ÿc8',
    'YELLOW': 'ÿc9',
    'PURPLE': 'ÿc;'
}


def color_handler(text, *args):
    return f'{COLOR_CODES[args[0].upper()]}{text}'


InstructionInvoker.default = InstructionInvoker()
InstructionInvoker.default.register('Text', replace_text_handler)
InstructionInvoker.default.register('Color', color_handler)
