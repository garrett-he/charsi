import os
import tempfile
from pathlib import Path

from click.testing import CliRunner

from charsi.strings import StringTable, LanguageTag
from charsi.commands.make import make_command


def test_cmd_make(cli_runner: CliRunner, path_presence_states_json: Path, path_recipe1_recipe: Path):
    tbl = StringTable()
    tbl.read(path_presence_states_json.open('r', encoding='utf-8-sig'))
    old = tbl.find('presenceMenus')

    result = cli_runner.invoke(make_command, ['--table-file', path_presence_states_json, '--', path_recipe1_recipe])

    if result.exception:
        print(result.output)

    assert not result.exception

    tmpfile = tempfile.mktemp()
    with open(tmpfile, 'w', encoding='utf-8-sig') as fp:
        fp.write(result.output)

    tbl = StringTable()
    with open(tmpfile, 'r', encoding='utf-8-sig') as fp:
        tbl.read(fp)

    os.unlink(tmpfile)

    s = tbl.find('presenceMenus')
    for tag in LanguageTag.tags():
        if tag == 'zhCN':
            assert s[tag] == 'Replaced_presenceMenus'
        else:
            assert s[tag] == old[tag]

    for s in tbl.findall('presenceA1Normal~presenceA5Hell'):
        for tag in LanguageTag.tags():
            assert s[tag] == 'Replaced'
