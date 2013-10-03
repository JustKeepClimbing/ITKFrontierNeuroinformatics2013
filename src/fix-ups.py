#!/usr/bin/env python

import os
from os.path import expanduser
import pickle
import sys

import git
from git.exc import GitCommandError


class FixUpCounter(object):

    fixup_days = 5
    fixup_seconds = fixup_days * 24 * 60 * 60

    def __init__(self, git_repo):
        self.git = git_repo
        # keep track of the the commits that have already been identified as
        # fixup commits so that they are not counted twice.
        self.fixup_commits = set()

    def fixup_counts(self, fromdate, todate):
        """Get the number of fixup commits per commit."""
        self.fixup_commits = set()
        commits_of_interest = self._commits_of_interest(fromdate, todate)

        number_of_commits = len(commits_of_interest)
        commit_index = 0

        commit_fixup_counts = dict()
        for commit in commits_of_interest:
            commit_index += 1
            sys.stdout.write('Analyzing commit ' + str(commit_index) + \
                    ' of ' + str(number_of_commits) + '\r')
            sys.stdout.flush()
            # Don't analyze the subsequent fixup-progression again.
            if commit in self.fixup_commits:
                continue
            changed_files = self._changed_files(commit)
            count = self._fixup_count(commit, changed_files)
            commit_fixup_counts[commit] = count
        return commit_fixup_counts, self.fixup_commits

    def _commits_of_interest(self, fromdate, todate):
        commits_of_interest = self.git.rev_list('HEAD',
                                                since=fromdate,
                                                until=todate,
                                                no_merges=True)
        commits_of_interest = commits_of_interest.split('\n')
        # chronological order
        commits_of_interest.reverse()
        return tuple(commits_of_interest)

    def _fixup_count(self, commit, changed_files):
        following_commits = self._following_commits(commit)
        hunks = self._hunks(commit, changed_files)
        count = 0
        for followup in following_commits:
            # Don't analyze the subsequent fixup-progression again.
            if followup in self.fixup_commits or not followup:
                continue
            fixed_files = self._was_fixed(hunks, followup)
            if fixed_files:
                follow_count = self._fixup_count(followup, fixed_files)
                self.fixup_commits.add(followup)
                count = max(follow_count + 1, count)
        return count

    def _changed_files(self, commit):
        git = self.git
        changed_files = git.diff(commit + '^!', diff_filter='AM',
                                 name_only=True)
        changed_files = changed_files.split('\n')
        # Do not track the submodule -- causes issues with git blame
        if 'Testing/Data' in changed_files:
            changed_files.remove('Testing/Data')
        if len(changed_files) == 1 and not changed_files[0]:
            return None
        return tuple(changed_files)

    def _following_commits(self, commit):
        git = self.git
        try:
            commit_date = git.show(commit, s=True, format="%ct")
        except GitCommandError:
            return tuple()
        until_date = int(commit_date) + self.fixup_seconds
        following_commits = git.rev_list(commit + '..',
                                         until=str(until_date),
                                         since=str(commit_date),
                                         no_merges=True)
        following_commits = following_commits.split('\n')
        # chronological order
        following_commits.reverse()
        return tuple(following_commits)

    def _hunks(self, commit, changed_files):
        git = self.git
        hunks = dict()
        if not changed_files:
            return hunks
        for changed_file in changed_files:
            try:
                blame = git.blame(commit + '^!', '--', changed_file,
                                  incremental=True)
            except GitCommandError:
                continue
            blame = blame.split('\n')
            hh = [tuple([int(x) for x in blame[0].split()[2:4]]),]
            blame = blame[1:]
            next_is_hunk = False
            for line in blame:
                if line.startswith('filename '):
                    next_is_hunk = True
                    continue
                if next_is_hunk:
                    next_is_hunk = False
                    line_split = line.split()
                    if line_split[0] != commit:
                        continue
                    hh.append(tuple([int(x) for x in line_split[2:4]]))

            hunks[changed_file] = (tuple(hh))
        return hunks

    def _was_fixed(self, hunks, followup):
        git = self.git
        followup_changed = git.diff(followup + '^!', diff_filter='M',
                                    name_only=True)
        followup_changed = followup_changed.split('\n')
        fixed_files = []
        for changed in followup_changed:
            if changed in hunks:
                added_lines = set()
                for hh in hunks[changed]:
                    added_lines.update(range(hh[0], hh[0] + hh[1]))
                try:
                    blame = git.blame(followup + '^!', '--',
                                      changed,
                                      incremental=True,
                                      reverse=True)
                except GitCommandError:
                    continue
                blame = blame.split('\n')
                first = blame[0].split()
                boundary = first[0]
                followup_deleted = set()
                followup_deleted.update(range(int(first[1]),
                                           int(first[1]) + int(first[3])))
                blame = blame[1:]
                next_is_hunk = False
                for line in blame:
                    if line.startswith('filename '):
                        next_is_hunk = True
                        continue
                    if next_is_hunk:
                        next_is_hunk = False
                        line_split = line.split()
                        if line_split[0] != boundary:
                            continue
                        followup_deleted.update(range(int(line_split[1]),
                                                   int(line_split[1]) + int(line_split[3])))
                if not followup_deleted.isdisjoint(added_lines):
                    fixed_files.append(changed)

        if len(fixed_files) > 0:
            return tuple(fixed_files)
        return None


home = expanduser('~')

# Assumed ITK git repository path.
repo_path = os.path.join(home, 'src', 'ITK')
repo = git.Repo(repo_path)
git_repo = repo.git

fixup_counter = FixUpCounter(git_repo)
# Gerrit use began August 25th, 2010.
print('Starting post-Gerrit analysis...')
fixup_counts, fixups = fixup_counter.fixup_counts('2010-08-25', '2013-08-25')
with open('PostGerrit.pkl', 'wb') as fp:
    pickle.dump((fixup_counts, fixups, 2), fp)
print('Starting pre-Gerrit analysis...')
fixup_counts, fixups = fixup_counter.fixup_counts('2007-08-25', '2010-08-25')
with open('PreGerrit.pkl', 'wb') as fp:
    pickle.dump((fixup_counts, fixups, 2), fp)
