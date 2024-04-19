import os
import shutil
import tempfile
from pathlib import Path

from click.testing import CliRunner

from charsi.commands.imbue import imbue_command
from charsi.strings import LanguageTag, StringTable


def test_cmd_imbue(cli_runner: CliRunner, path_presence_states_json: Path, path_recipe1_recipe: Path):
    workdir = Path(tempfile.mkdtemp())

    strings_dir = workdir.joinpath('local', 'lng', 'strings')
    strings_dir.mkdir(parents=True)

    shutil.copy(path_presence_states_json, strings_dir)

    recipes_dir = workdir.joinpath('recipes')
    recipes_dir.mkdir(parents=True)

    shutil.copy(path_recipe1_recipe, recipes_dir.joinpath('presence-states.recipe'))

    tbl = StringTable()
    with strings_dir.joinpath('presence-states.json').open('r', encoding='utf-8-sig') as fp:
        tbl.read(fp)
    old = tbl.find('presenceMenus').copy()

    os.chdir(workdir)

    result = cli_runner.invoke(imbue_command, ['--target-dir', str(workdir)])
    assert not result.exception

    tbl = StringTable()
    with strings_dir.joinpath('presence-states.json').open('r', encoding='utf-8-sig') as fp:
        tbl.read(fp)
    new = tbl.find('presenceMenus')
    for lang in LanguageTag.tags():
        if lang == 'zhCN':
            assert new[lang] == 'Replaced_presenceMenus'
        else:
            assert new[lang] == old[lang]

    for item in tbl.findall('presenceA1Normal~presenceA5Hell'):
        for lang in LanguageTag.tags():
            assert item[lang] == 'Replaced'

    shutil.rmtree(workdir)
