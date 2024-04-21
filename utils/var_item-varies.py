#!/usr/bin/env python

import sqlite3
from cauldron.core import PropertyTable


def dict_factory(cursor, row):
    return {col[0]: row[i] for i, col in enumerate(cursor.description)}


alias = {}
db = sqlite3.connect('d2excel.db')
db.row_factory = dict_factory


def main():
    prop_alias = PropertyTable()
    prop_alias.load('item-props.alias')


if __name__ == '__main__':
    main()
