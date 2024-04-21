#!/usr/bin/env python

import sqlite3


def dict_factory(cursor, row):
    return {col[0]: row[i] for i, col in enumerate(cursor.description)}


alias = {}
conn = sqlite3.connect('d2data.sqlite')
conn.row_factory = dict_factory


def main():
    sql = "SELECT * FROM levels"
    names = []
    for row in conn.cursor().execute(sql).fetchall():
        if row['MonLvlEx(H)'] is None:
            continue
        names.append(row['LevelName'])

    print(', '.join(names))


if __name__ == '__main__':
    main()
