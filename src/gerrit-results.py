#!/usr/bin/env python

"""Quantitative output for Gerrit Results section."""

import json

gerrit_results = {}

with open('../data/gerrit_data.json', 'r') as fp:
    gerrit_data = json.load(fp)

changes = gerrit_data['changes']

gerrit_results['changes'] = len(changes)

reviews = 0
for change in changes:
    for patch_set in change['patchSets']:
        for approval in patch_set.get('approvals', []):
            if approval['description'] == 'Code Review':
                reviews += 1
gerrit_results['reviews'] = reviews


with open('gerrit_results.json', 'wb') as fp:
    json.dump(gerrit_results, fp)
