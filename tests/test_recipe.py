import importlib.resources
from pathlib import Path

from charsi.recipe import Recipe
from charsi.strings import StringTable, LanguageTag


def test_recipe_read():
    recipe = Recipe()
    recipe.read(importlib.resources.files('tests.res').joinpath('recipe1.recipe').open('r', encoding='utf-8'))

    assert len(recipe.instructions) == 2
    assert recipe.instructions[0].name == 'Text'
    assert recipe.instructions[0].query == 'presenceMenus'
    assert len(recipe.instructions[0].args) == 1
    assert recipe.instructions[0].args[0] == 'Replaced_presenceMenus'

    assert recipe.instructions[1].name == 'Text'
    assert recipe.instructions[1].query == 'presenceA1Normal~presenceA5Hell'
    assert len(recipe.instructions[1].args) == 1
    assert recipe.instructions[1].args[0] == 'Replaced'


def test_recipe_build(presence_states: Path):
    recipe = Recipe()
    recipe.read(importlib.resources.files('tests.res').joinpath('recipe1.recipe').open('r', encoding='utf-8'))

    tbl = StringTable()
    tbl.read(presence_states.open('r', encoding='utf-8-sig'))

    old = tbl.find('presenceMenus').copy()

    recipe.build(tbl)

    new = tbl.find('presenceMenus')
    for lang in LanguageTag.tags():
        if lang == 'zhCN':
            assert new[lang] == 'Replaced_presenceMenus'
        else:
            assert new[lang] == old[lang]

    for item in tbl.findall('presenceA1Normal~presenceA5Hell'):
        for lang in LanguageTag.tags():
            assert item[lang] == 'Replaced'


def test_recipe_tag(presence_states: Path):
    recipe = Recipe()
    recipe.read(importlib.resources.files('tests.res').joinpath('recipe2.recipe').open('r', encoding='utf-8'))

    tbl = StringTable()
    tbl.read(presence_states.open('r', encoding='utf-8-sig'))

    old1 = tbl.find('presenceMenus').copy()
    old2 = tbl.find('presenceA1Normal').copy()

    recipe.build(tbl)

    new1 = tbl.find('presenceMenus')
    new2 = tbl.find('presenceA1Normal')

    for lang in LanguageTag.tags():
        if lang == 'zhCN':
            assert new1[lang] == 'Replaced_presenceMenus'
        else:
            assert new1[lang] == old1[lang]

        if lang == 'enUS':
            assert new2[lang] == 'Replaced_presenceA1Normal'
        else:
            assert new2[lang] == old2[lang]
