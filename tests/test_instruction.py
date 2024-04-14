import importlib.resources

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

    with pytest.raises(InstructionFormatError) as e:
        parse('Invalid Instruction')

    assert str(e.value) == 'Invalid Instruction'

    with pytest.raises(InstructionFormatError) as e:
        parse('Invalid Instruction:')

    assert str(e.value) == 'Invalid Instruction:'


def test_instruction_invoker():
    def handler(text: str, *args):
        return f'{text}:{"_".join(args)}'

    invoker = InstructionInvoker()
    inst = parse('TestInstruction[query]: arg1, arg2')

    invoker.register('TestInstruction', handler)
    assert invoker.is_registered('TestInstruction')

    with pytest.raises(InstructionConflictError) as e:
        invoker.register('TestInstruction', handler)
    assert str(e.value) == 'TestInstruction'

    invoker.unregister('TestInstruction')
    assert not invoker.is_registered('TestInstruction')

    with pytest.raises(InstructionUndefinedError) as e:
        invoker.invoke(inst, '')
    assert str(e.value) == 'TestInstruction'

    with pytest.raises(InstructionUndefinedError) as e:
        invoker.unregister('TestInstruction')
    assert str(e.value) == 'TestInstruction'

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


def test_instruction_invoker_lua():
    invoker = InstructionInvoker()
    invoker.load_lua(importlib.resources.files('tests.res').joinpath('test.lua').read_text())

    inst = parse('LuaInstruction[test]: target-text')
    assert invoker.invoke(inst, 'origin-text') == 'LuaInstruction:origin-text:target-text'
