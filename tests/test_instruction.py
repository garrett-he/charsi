from pathlib import Path

import pytest
from charsi.instruction import parse, InstructionFormatError, InstructionInvoker, InstructionConflictError, \
    InstructionUndefinedError


def test_instruction_parse():
    inst = parse('TestInstruction[query][lang1]: arg1, arg2, arg3 # comment')
    assert inst.name == 'TestInstruction'
    assert inst.query == 'query'
    assert inst.lang == 'lang1'
    assert len(inst.args) == 3
    assert inst.args[0] == 'arg1' and inst.args[1] == 'arg2' and inst.args[2] == 'arg3'

    with pytest.raises(InstructionFormatError) as exc:
        parse('Invalid Instruction')

    assert str(exc.value) == 'Invalid Instruction'

    with pytest.raises(InstructionFormatError) as exc:
        parse('Invalid Instruction:')

    assert str(exc.value) == 'Invalid Instruction:'


def test_instruction_invoker():
    def handler(text: str, *args):
        return f'{text}:{"_".join(args)}'

    invoker = InstructionInvoker()
    inst = parse('TestInstruction[query]: arg1, arg2')

    invoker.register('TestInstruction', handler)
    assert invoker.is_registered('TestInstruction')

    with pytest.raises(InstructionConflictError) as exc:
        invoker.register('TestInstruction', handler)
    assert str(exc.value) == 'TestInstruction'

    invoker.unregister('TestInstruction')
    assert not invoker.is_registered('TestInstruction')

    with pytest.raises(InstructionUndefinedError) as exc:
        invoker.invoke(inst, '')
    assert str(exc.value) == 'TestInstruction'

    with pytest.raises(InstructionUndefinedError) as exc:
        invoker.unregister('TestInstruction')
    assert str(exc.value) == 'TestInstruction'

    invoker.register('TestInstruction', handler)
    assert invoker.invoke(inst, 'TestString') == 'TestString:arg1_arg2'


def test_default_instruction_invoker():
    invoker = InstructionInvoker.default

    inst = parse('Text[query]: text-replaced')
    result = invoker.invoke(inst, 'origin-text')
    assert result == 'text-replaced'

    inst = parse('Color[query]: White')
    result = invoker.invoke(inst, 'origin-text')
    assert result == 'ÿc0origin-text'


def test_instruction_invoker_lua(path_instructions_lua: Path):
    invoker = InstructionInvoker()
    invoker.load_lua(path_instructions_lua.read_text(encoding='utf-8'))

    inst = parse('LuaInstruction[test]: target-text')
    assert invoker.invoke(inst, 'origin-text') == 'LuaInstruction:origin-text:target-text'
