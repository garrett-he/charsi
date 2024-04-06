from charsi.utils import split_text


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
