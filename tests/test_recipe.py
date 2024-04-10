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
    assert recipe.instructions[1].query == 'presenceA1Normal'
    assert len(recipe.instructions[1].args) == 1
    assert recipe.instructions[1].args[0] == 'Replaced_presenceA1Normal'


def test_recipe_build(presence_states: Path):
    recipe = Recipe()
    recipe.read(importlib.resources.files('tests.res').joinpath('recipe1.recipe').open('r', encoding='utf-8'))

    tbl = StringTable()
    tbl.read(presence_states.open('r', encoding='utf-8-sig'))

    recipe.build(tbl)

    new = tbl.find('presenceMenus')
    for lang in LanguageTag.tags():
        assert new[lang] == 'Replaced_presenceMenus'

    new = tbl.find('presenceA1Normal')
    for lang in LanguageTag.tags():
        assert new[lang] == 'Replaced_presenceA1Normal'
