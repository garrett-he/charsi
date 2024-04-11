import sys
from typing import IO

import click

from charsi.strings import StringTable
from charsi.recipe import Recipe


@click.command('imbue')
@click.option('--table-file', help='Path of string table file.', metavar='FILE', type=click.File(mode='r', encoding='utf-8-sig'), required=True)
@click.argument('recipe-file', metavar='FILE', type=click.File(mode='r', encoding='utf-8-sig'), required=True)
def imbue_command(table_file: IO, recipe_file: IO):
    """Build a string table with the specified recipe."""

    recipe = Recipe()
    recipe.read(recipe_file)

    tbl = StringTable()
    tbl.read(table_file)

    recipe.build(tbl)
    tbl.dump(sys.stdout)
