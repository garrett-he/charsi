#!/usr/bin/env python

import sqlite3


def dict_factory(cursor, row):
    return {col[0]: row[i] for i, col in enumerate(cursor.description)}


alias = {}
conn = sqlite3.connect('d2excel.db')
conn.row_factory = dict_factory


def get_codes(sql, col):
    return [row[col] for row in conn.cursor().execute(sql)]


def to_text(codes):
    return ', '.join(codes)


def armor_codes(rank):
    return get_codes("SELECT code FROM armor WHERE code = %s" % rank, 'code')


def weapon_codes(rank):
    return get_codes("SELECT code FROM weapons WHERE code = %s" % rank, 'code')


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


def main():
    alias['Normal Armor'] = to_text(armor_codes('normcode'))
    alias['Normal Weapons'] = to_text(weapon_codes('normcode'))
    alias['Normal Items'] = 'Normal Armor, Normal Weapons'

    alias['Exceptional Armor'] = to_text(armor_codes('ubercode'))
    alias['Exceptional Weapons'] = to_text(weapon_codes('ubercode'))
    alias['Exceptional Items'] = 'Exceptional Armor, Exceptional Weapons'

    alias['Elite Armor'] = to_text(armor_codes('ultracode'))
    alias['Elite Weapons'] = to_text(weapon_codes('ultracode'))
    alias['Elite Items'] = 'Elite Armor, Elite Weapons'

    alias['Normal Unique Armor'] = to_text(unique_armor_codes('normcode'))
    alias['Normal Unique Weapons'] = to_text(unique_weapon_codes('normcode'))
    alias['Normal Unique Items'] = 'Normal Unique Armor, Normal Unique Weapons'

    alias['Exceptional Unique Armor'] = to_text(unique_armor_codes('ubercode'))
    alias['Exceptional Unique Weapons'] = to_text(unique_weapon_codes('ubercode'))
    alias['Exceptional Unique Items'] = 'Exceptional Unique Armor, Exceptional Unique Weapons'

    alias['Elite Unique Armor'] = to_text(unique_armor_codes('ultracode'))
    alias['Elite Unique Weapons'] = to_text(unique_weapon_codes('ultracode'))
    alias['Elite Unique Items'] = 'Elite Unique Armor, Elite Unique Weapons'

    alias['Unique Rings'] = to_text(unique_ring_codes())
    alias['Unique Amulets'] = to_text(unique_amulet_codes())
    alias['Unique Charms'] = to_text(unique_charm_codes())
    alias['Unique Jewels'] = 'Rainbow Facet'

    alias['Normal Set Armor'] = to_text(set_armor_codes('normcode'))
    alias['Normal Set Weapons'] = to_text(set_weapon_codes('normcode'))
    alias['Normal Set Items'] = 'Normal Set Armor, Normal Set Weapons'

    alias['Exceptional Set Armor'] = to_text(set_armor_codes('ubercode'))
    alias['Exceptional Set Weapons'] = to_text(set_weapon_codes('ubercode'))
    alias['Exceptional Set Items'] = 'Exceptional Set Armor, Exceptional Set Weapons'

    alias['Elite Set Armor'] = to_text(set_armor_codes('ultracode'))
    alias['Elite Set Weapons'] = to_text(set_weapon_codes('ultracode'))
    alias['Elite Set Items'] = 'Elite Set Armor, Elite Set Weapons'

    alias['Set Rings'] = to_text(set_ring_codes())
    alias['Set Amulets'] = to_text(set_amulet_codes())

    alias['Set Items'] = 'Normal Set Items, Exceptional Set Items, Elite Set Items, Set Rings, Set Amulets'

    alias['Chipped Gems'] = to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem0'", 'code'))
    alias['Flawed Gems'] = to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem1'", 'code'))
    alias['Normal Gems'] = to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem2'", 'code'))
    alias['Flawless Gems'] = to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem3'", 'code'))
    alias['Perfect Gems'] = to_text(get_codes("SELECT code FROM misc WHERE type2 = 'gem4'", 'code'))

    alias['Runes'] = to_text(get_codes("SELECT code FROM misc WHERE type = 'rune'", 'code'))
    alias['RunesL'] = to_text([c + 'L' for c in get_codes("SELECT code FROM misc WHERE type = 'rune'", 'code')])

    for key in alias:
        print('%s = %s' % (key, alias[key]))


if __name__ == '__main__':
    main()
