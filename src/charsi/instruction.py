from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

from .utils import split_text


def parse(text: str) -> Instruction:
    fds = split_text(split_text(text, '#')[0], ':')
    if len(fds) < 2:
        raise InstructionFormatError(text)

    m = re.match(r'^\s*(\w+)\s*(\[[^]]+])', fds[0])

    if not m:
        raise InstructionFormatError(text)

    return Instruction(
        name=m.group(1),
        query=m.group(2).strip(' []'),
        args=[arg.strip() for arg in fds[1].split(',')]
    )


@dataclass
class Instruction:
    name: str
    query: str
    args: List[str]


class _InstructionError(Exception):
    ...


class InstructionFormatError(_InstructionError):
    ...
