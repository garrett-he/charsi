#!/usr/bin/env python
import sqlite3
from pathlib import Path
from typing import List

import click

db: sqlite3.Connection


def dict_factory(cursor: sqlite3.Cursor, row: List):
    return {col[0]: row[i] for i, col in enumerate(cursor.description)}


def get_codes(sql: str, col: str):
    return [row[col] for row in db.cursor().execute(sql)]


def to_text(codes: List[str]):
    return ', '.join(codes)


def armor_codes(rank: str):
    return get_codes(f'SELECT code FROM armor WHERE code = {rank}', 'code')


def weapon_codes(rank):
    return get_codes(f'SELECT code FROM weapons WHERE code = {rank}', 'code')


def unique_armor_codes(rank):
    sql = "SELECT \"index\" FROM uniqueitems WHERE code IN ('%s')" % "','".join(armor_codes(rank))
    return get_codes(sql, 'index')


def unique_weapon_codes(rank):
    sql = "SELECT \"index\" FROM uniqueitems WHERE code IN ('%s')" % "','".join(weapon_codes(rank))
    return get_codes(sql, 'index')


def unique_ring_codes():
    sql = "SELECT \"index\" FROM uniqueitems WHERE code = 'rin'"
    return get_codes(sql, 'index')


def unique_amulet_codes():
    sql = "SELECT \"index\" FROM uniqueitems WHERE code = 'amu'"
    return get_codes(sql, 'index')


def unique_charm_codes():
    sql = "SELECT \"index\" FROM uniqueitems WHERE code IN ('cm1', 'cm2', 'cm3')"
    return get_codes(sql, 'index')


def set_armor_codes(rank):
    sql = "SELECT \"index\" FROM setitems WHERE item IN ('%s')" % "','".join(armor_codes(rank))
    return get_codes(sql, 'index')


def set_weapon_codes(rank):
    sql = "SELECT \"index\" FROM setitems WHERE item IN ('%s')" % "','".join(weapon_codes(rank))
    return get_codes(sql, 'index')


def set_ring_codes():
    sql = "SELECT \"index\" FROM setitems WHERE item = 'rin'"
    return get_codes(sql, 'index')


def set_amulet_codes():
    sql = "SELECT \"index\" FROM setitems WHERE item = 'amu'"
    return get_codes(sql, 'index')


@click.command()
@click.option('--database', help='Path of d2txt database.', type=click.Path(exists=True, dir_okay=False), required=True)
def main(database: Path | str):
    global db

    db = sqlite3.connect(database)
    db.row_factory = dict_factory

    alias = {
        'Normal Armor': to_text(armor_codes('normcode')),
        'Normal Weapons': to_text(weapon_codes('normcode')),
        'Normal Items': 'Normal Armor, Normal Weapons',
        'Exceptional Armor': to_text(armor_codes('ubercode')),
        'Exceptional Weapons': to_text(weapon_codes('ubercode')),
        'Exceptional Items': 'Exceptional Armor, Exceptional Weapons',
        'Elite Armor': to_text(armor_codes('ultracode')),
        'Elite Weapons': to_text(weapon_codes('ultracode')),
        'Elite Items': 'Elite Armor, Elite Weapons',
        'Normal Unique Armor': to_text(unique_armor_codes('normcode')),
        'Normal Unique Weapons': to_text(unique_weapon_codes('normcode')),
        'Normal Unique Items': 'Normal Unique Armor, Normal Unique Weapons',
        'Exceptional Unique Armor': to_text(unique_armor_codes('ubercode')),
        'Exceptional Unique Weapons': to_text(unique_weapon_codes('ubercode')),
        'Exceptional Unique Items': 'Exceptional Unique Armor, Exceptional Unique Weapons',
        'Elite Unique Armor': to_text(unique_armor_codes('ultracode')),
        'Elite Unique Weapons': to_text(unique_weapon_codes('ultracode')),
        'Elite Unique Items': 'Elite Unique Armor, Elite Unique Weapons',
        'Unique Rings': to_text(unique_ring_codes()),
        'Unique Amulets': to_text(unique_amulet_codes()),
        'Unique Charms': to_text(unique_charm_codes()),
        'Unique Jewels': 'Rainbow Facet',
        'Normal Set Armor': to_text(set_armor_codes('normcode')),
        'Normal Set Weapons': to_text(set_weapon_codes('normcode')),
        'Normal Set Items': 'Normal Set Armor, Normal Set Weapons',
        'Exceptional Set Armor': to_text(set_armor_codes('ubercode')),
        'Exceptional Set Weapons': to_text(set_weapon_codes('ubercode')),
        'Exceptional Set Items': 'Exceptional Set Armor, Exceptional Set Weapons',
        'Elite Set Armor': to_text(set_armor_codes('ultracode')),
        'Elite Set Weapons': to_text(set_weapon_codes('ultracode')),
        'Elite Set Items': 'Elite Set Armor, Elite Set Weapons',
        'Set Rings': to_text(set_ring_codes()),
        'Set Amulets': to_text(set_amulet_codes()),
        'Set Items': 'Normal Set Items, Exceptional Set Items, Elite Set Items, Set Rings, Set Amulets',
        'Chipped Gems': to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem0'", 'code')),
        'Flawed Gems': to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem1'", 'code')),
        'Normal Gems': to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem2'", 'code')),
        'Flawless Gems': to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem3'", 'code')),
        'Perfect Gems': to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem4'", 'code')),
        'Runes': to_text(get_codes("SELECT code FROM misc WHERE type = 'rune'", 'code')),
        'RunesL': to_text([c + 'L' for c in get_codes("SELECT code FROM misc WHERE type = 'rune'", 'code')])}

    for key in alias:
        print('%s = %s' % (key, alias[key]))


if __name__ == '__main__':
    main()
