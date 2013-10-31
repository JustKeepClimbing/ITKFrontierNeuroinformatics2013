#!/usr/bin/env python

"""Plot the number of submissions and reviews to the Insight Journal over the
years."""

import os
import sys

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import prettyplotlib

import brewer2mpl
set2 = brewer2mpl.get_map('Set2', 'qualitative', 8).mpl_colors

mpl.rcParams['font.size'] = 10

mpl.rcParams['axes.labelsize'] = 'x-large'
mpl.rcParams['xtick.labelsize'] = 'large'
mpl.rcParams['ytick.labelsize'] = 'large'
mpl.rcParams['legend.fontsize'] = 'x-large'
mpl.rcParams['figure.dpi'] = 900


def plot_submissions(data, outputfile=None):
    fig, ax = plt.subplots(1)

    prettyplotlib.bar(ax, [y - 0.4 for y in data['year']], data['submissions'],
            label='Submissions', width=0.4, color=set2[2], grid='y')
    prettyplotlib.bar(ax, data['year'], data['reviews'],
            label='Reviews', width=0.4, color=set2[3], grid='y')
    ax.set_xticks(data['year'])
    ax.set_xticklabels([str(y) for y in data['year']])
    ax.set_xlabel('Year')
    ax.set_xlim(data['year'][0] - 1, data['year'][-1] + 1)
    plt.legend(loc='upper left')

    if outputfile:
        fig.savefig(outputfile)
    else:
        plt.show()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] +
              ' <data.csv> [output_file.eps]')
        sys.exit(1)

    csv_file = sys.argv[1]
    data = mpl.mlab.csv2rec(csv_file)

    if len(sys.argv) > 2:
        outputfile = sys.argv[2]
        dirname = os.path.dirname(outputfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    else:
        outputfile = None

    plot_submissions(data, outputfile)
