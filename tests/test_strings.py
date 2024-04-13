import os
import tempfile
from pathlib import Path

import pytest
from charsi.strings import StringTable


def test_stringtable_read_and_write(presence_states: Path):
    tbl = StringTable()
    items = tbl.items

    assert len(items) == 0

    tbl.read(presence_states.open('r', encoding='utf-8-sig'))

    assert items == tbl.items
    assert len(items) == 16
    assert tbl.items[0]['id'] == 26047
    assert tbl.items[0]['Key'] == 'presenceMenus'

    tbl.items[0]['id'] = 12345
    tbl.items[0]['Key'] = 'TestKey'

    tmpfile = tempfile.mktemp()

    with open(tmpfile, 'w', encoding='utf-8-sig') as fp:
        tbl.write(fp)

    with open(tmpfile, 'r', encoding='utf-8-sig') as fp:
        tmp_tbl = StringTable()
        tmp_tbl.read(fp)

    assert len(tbl.items) == 16
    assert tmp_tbl.items[0]['id'] == 12345
    assert tmp_tbl.items[0]['Key'] == 'TestKey'

    os.unlink(tmpfile)


def test_stringtable_find(presence_states: Path):
    tbl = StringTable()
    tbl.read(presence_states.open('r', encoding='utf-8-sig'))

    item = tbl.find('presenceMenus')
    assert item['id'] == 26047 and item['Key'] == 'presenceMenus'

    with pytest.raises(IndexError) as e:
        tbl.find('nonExists')

    assert str(e.value) == 'nonExists'


def test_stringtable_findall(presence_states):
    tbl = StringTable()
    tbl.read(presence_states.open('r', encoding='utf-8-sig'))

    sl = tbl.findall('presenceMenus, presenceA1Normal~presenceA5Hell')

    assert len(sl) == 16
    assert sl[0]['Key'] == 'presenceMenus'
    assert sl[1]['Key'] == 'presenceA1Normal'
    assert sl[6]['Key'] == 'presenceA1Nightmare'
    assert sl[11]['Key'] == 'presenceA1Hell'
    assert sl[15]['Key'] == 'presenceA5Hell'

    with pytest.raises(IndexError) as e:
        tbl.findall('notExists1~notExists2')

    assert str(e.value) == 'notExists1~notExists2'

    sl = tbl.findall('presenceMenus')
    assert len(sl) == 1
    assert sl[0]['Key'] == 'presenceMenus'

    with pytest.raises(LookupError) as e:
        tbl.findall('nonExists')

    assert str(e.value) == 'nonExists'

    with pytest.raises(IndexError) as e:
        tbl.findall('presenceA5Hell~presenceA1Normal')
    assert str(e.value) == 'presenceA5Hell~presenceA1Normal'


def test_stringtable_dump(presence_states: Path):
    tbl = StringTable()
    tbl.read(presence_states.open('r', encoding='utf-8-sig'))

    tmpfile = tempfile.mktemp()

    with open(tmpfile, 'w', encoding='utf-8-sig') as fp:
        tbl.dump(fp)

    with open(tmpfile, 'r', encoding='utf-8-sig') as fp:
        tmp_tbl = StringTable()
        tmp_tbl.read(fp)

    assert len(tbl.items) == 16
    assert tbl.items[0]['id'] == 26047
    assert tbl.items[0]['Key'] == 'presenceMenus'
