#!/usr/bin/env python

import json
import sys
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import prettyplotlib
import numpy as np

mpl.rcParams['axes.labelsize'] = 'x-large'
mpl.rcParams['xtick.labelsize'] = 'large'
mpl.rcParams['ytick.labelsize'] = 'large'
mpl.rcParams['figure.dpi'] = 900


def plot_contributors(contributors, outputfile=None):
    number_of_commits = []
    contributor_anonymous = []
    count = 1
    for contributor in contributors:
        contributor_commits = contributor.split()[0]
        number_of_commits.append(int(contributor_commits))
        contributor_anonymous.append(count)
        count = count+1
    fig = plt.figure()
    ax = fig.add_subplot(111)
    max_number_of_commits=np.max(number_of_commits)
    contributors = range(0,max_number_of_commits-1)
    prettyplotlib.bar(ax, contributor_anonymous, number_of_commits, width=0.9, grid='y')
    ax.set_xlabel('ITK Contributors')
    ax.set_ylabel('Number of Commits')
    ax.set_xlim(0, 100)
    if outputfile:
        fig.savefig(outputfile)
    else:
        plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] +
              ' <itk_git_contributors.dat> [output_file.eps]')
        sys.exit(1)

    itk_git_contributors = sys.argv[1]
    with open(itk_git_contributors, 'r') as fp:
        data = fp.readlines()
    if len(sys.argv) > 2:
        outputfile = sys.argv[2]
        dirname = os.path.dirname(outputfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    else:
        outputfile = None
    plot_contributors(data, outputfile)
