#!/usr/bin/env python

"""Quantitative output for Gerrit Results section."""

import json

with open('../data/gerrit_data.json', 'r') as fp:
    gerrit_data = json.load(fp)

changes = gerrit_data['changes']

### @export "changes"
print(len(changes))
