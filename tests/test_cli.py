import os
import importlib.metadata
import importlib.resources
import tempfile
from pathlib import Path

import click.testing
import click

from charsi.__main__ import cli
from charsi.strings import StringTable, LanguageTag
from charsi.commands.make import make_command


def test_cli(cli_runner: click.testing.CliRunner):
    result = cli_runner.invoke(cli, ['--version'])

    if result.exception:
        print(result.output)

    assert not result.exception
    assert result.output.strip() == importlib.metadata.version('charsi')


def test_cli_make_command(cli_runner: click.testing.CliRunner, presence_states: Path):
    tbl = StringTable()
    tbl.read(presence_states.open('r', encoding='utf-8-sig'))
    old = tbl.find('presenceMenus')

    recipe_file = importlib.resources.files('tests.res').joinpath('recipe1.recipe')

    result = cli_runner.invoke(make_command, ['--table-file', presence_states, '--', recipe_file])

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

    s = tbl.find('presenceA1Normal')
    for tag in LanguageTag.tags():
        assert s[tag] == 'Replaced_presenceA1Normal'
