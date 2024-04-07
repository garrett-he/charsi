import pytest
from charsi.instruction import parse, InstructionFormatError, InstructionInvoker, InstructionConflictError, InstructionUndefinedError


def test_instruction_parse():
    inst = parse('TestInstruction[query]: arg1, arg2, arg3 # comment')
    assert inst.name == 'TestInstruction'
    assert inst.query == 'query'
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
