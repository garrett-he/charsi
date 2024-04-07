from charsi.utils import split_text, filter_irrelevant_lines


def test_split_text():
    fds = split_text(' Test ', ':')
    assert len(fds) == 1
    assert fds[0] == 'Test'

    fds = split_text(' Test : value1, value2 ', ':')
    assert len(fds) == 2
    assert fds[0] == 'Test'
    assert fds[1] == 'value1, value2'

    fds = split_text(' Test : value1, value2 ', ',')
    assert len(fds) == 2
    assert fds[0] == 'Test : value1'
    assert fds[1] == 'value2'


def test_filter_irrelevant_lines():
    text = '''

# comment1

line1
  line2

line3 # comment2

# comment3

'''

    lines = list(filter_irrelevant_lines(text.split('\n')))

    assert len(lines) == 3
    assert lines[0] == 'line1'
    assert lines[1] == 'line2'
    assert lines[2] == 'line3 # comment2'
