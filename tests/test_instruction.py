import pytest
from charsi.instruction import parse, InstructionFormatError


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
