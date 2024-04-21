#!/usr/bin/env python

import sqlite3


def dict_factory(cursor, row):
    return {col[0]: row[i] for i, col in enumerate(cursor.description)}


alias = {}
conn = sqlite3.connect('d2excel.db')
conn.row_factory = dict_factory


def main():
    sql = "SELECT code FROM misc WHERE type = 'rune' ORDER BY code"
    rows = conn.cursor().execute(sql).fetchall()

    for i in range(len(rows)):
        print('%s = %d' % (rows[i]['code'], i + 1))
        print('%sL = %d' % (rows[i]['code'], i + 1))


if __name__ == '__main__':
    main()
