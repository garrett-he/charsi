#!/usr/bin/env python
import json

filename = '/opt/games/bnet/Diablo II Resurrected/Mods/Enlight/Enlight.mpq/data/local/lng/strings/item-names.json'
strings = json.loads(open(filename, 'r').read())

for item in map(lambda x: x.split('='), filter(lambda x: x != '' and x[0] != '#', map(lambda x: x.strip(), open('item_varies.txt', 'r').readlines()))):
    key = item[0]
    varies = item[1]

    for string in strings:
        if string['Key'] == key:
            string['enUS'] = '%s [%s]' % (string['enUS'], varies)

print(json.dumps(strings, ensure_ascii=False, indent=4))