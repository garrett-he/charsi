from os import PathLike, path, getcwd, getenv
from glob import glob

import click

from charsi.strings import StringTable
from charsi.recipe import Recipe


@click.command('imbue')
@click.option('--target-dir', help='Path of target directory.', type=click.Path(file_okay=False), required=False)
def imbue_command(target_dir: PathLike):
    """Build recipes by conventions under current directory."""

    target_dir = target_dir is None and target_dir or getenv('CHARSI_TARGET_DIR')

    if target_dir is None:
        raise NotADirectoryError('Target directory not specified.')

    for recipe_file in glob(path.join(getcwd(), '**/*.recipe'), recursive=True):
        tbl_file = path.join(target_dir, 'local/lng/strings', f'{path.basename(recipe_file).split(".")[0]}.json')
        tbl = StringTable()
        with open(tbl_file, 'r', encoding='utf-8-sig') as fp:
            tbl.read(fp)

        recipe = Recipe()
        with open(recipe_file, 'r', encoding='utf-8') as fp:
            recipe.read(fp)

        recipe.build(tbl)

        with open(tbl_file, 'w', encoding='utf-8-sig') as fp:
            tbl.dump(fp)
