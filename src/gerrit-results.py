#!/usr/bin/env python

"""Quantitative output for Gerrit Results section."""

import json
import numpy as np

gerrit_results = {}

with open('../data/gerrit_data.json', 'r') as fp:
    gerrit_data = json.load(fp)

changes = gerrit_data['changes']

gerrit_results['changes'] = len(changes)

reviews = 0
max_reviews = 0
for change in changes:
    for patch_set in change['patchSets']:
        for approval in patch_set.get('approvals', []):
            if approval['description'] == 'Code Review':
                reviews += 1
    if len(change['patchSets']) > max_reviews:
        max_reviews = len(change['patchSets'])
gerrit_results['reviews'] = reviews
gerrit_results['max_reviews'] = max_reviews


with open('gerrit_results.json', 'wb') as fp:
    json.dump(gerrit_results, fp)
