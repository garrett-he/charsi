#!/usr/bin/env python3
import os
import csv
import click
import sqlite3
from glob import glob
from pathlib import Path


def import_txt_file(db: sqlite3.Connection, filepath: str):
    tb_name = os.path.basename(filepath).split('.')[0]

    with open(filepath, 'r', encoding='cp949') as fp:
        reader = csv.reader(fp, dialect='excel-tab', quoting=csv.QUOTE_NONE, quotechar=None)

        cols = next(reader)

        sql = 'CREATE TABLE "%s" (%s)' % (tb_name, ',\n'.join(map(lambda col: f'"{col}" TEXT NULL', cols)))
        db.execute(sql)

        for row in reader:
            sql = 'INSERT INTO "%s" VALUES(%s)' % (tb_name, ','.join(map(lambda x: (x is None or x == '' or x == 'NULL') and 'NULL' or '"%s"' % x.replace('"', '""'), row)))
            db.execute(sql)

    db.commit()


@click.command()
@click.option('--text-dir', help='Path of directory contains .txt files', type=click.Path(exists=True, file_okay=False), required=True)
@click.option('--version', help='Game version of .txt files', type=str, required=False, default='unknown', metavar='VERSION')
def main(text_dir: Path, version: str):
    """This script creates a SQLite database contains game data of *.txt files extracted from /data/global/excel"""

    text_dir = Path(text_dir)
    db_path = Path(f'd2data_{version}.db')

    if db_path.exists():
        raise FileExistsError(db_path)

    db = sqlite3.connect(db_path)

    for filename in glob(f'{text_dir}/*.txt'):
        import_txt_file(db, filename)

    db.close()


if __name__ == '__main__':
    main()
