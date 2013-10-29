#!/usr/bin/env python

"""Quantitative output for Gerrit Results section."""

import json
import os
import subprocess

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

cwd = os.getcwd()
itk_src = os.path.join(os.getenv('HOME'), 'src', 'ITK')
os.chdir(itk_src)
pre_gerrit_commits = subprocess.check_output(['git',
    'rev-list',
    'HEAD',
    '--since=2007-08-25',
    '--until=2010-08-25',
    '--no-merges',
    '--count'])
gerrit_results['pre_gerrit_commits'] = pre_gerrit_commits.strip()
post_gerrit_commits = subprocess.check_output(['git',
    'rev-list',
    'HEAD',
    '--since=2010-08-25',
    '--until=2013-08-25',
    '--no-merges',
    '--count'])
gerrit_results['post_gerrit_commits'] = post_gerrit_commits.strip()
os.chdir(cwd)

with open('gerrit_results.json', 'wb') as fp:
    json.dump(gerrit_results, fp)
