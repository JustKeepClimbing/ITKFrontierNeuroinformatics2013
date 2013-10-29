#!/usr/bin/env python

import json
import pickle
import sys
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

import brewer2mpl
set2 = brewer2mpl.get_map('Set2', 'qualitative', 8).mpl_colors

#mpl.rcdefaults()
mpl.rcParams['axes.labelsize'] = 'x-large'
mpl.rcParams['xtick.labelsize'] = 'large'
mpl.rcParams['ytick.labelsize'] = 'large'
mpl.rcParams['legend.fontsize'] = 'x-large'
#mpl.rcParams['figure.dpi'] = 900


def plot_fixups(pre_gerrit, post_gerrit, outputfile=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fixup_range = (0, 6)
    bins = fixup_range[1]
    colors = [c + (0.5,) for c in set2[0:2]]
    print(pre_gerrit)
    percent, bins, patches = ax.hist([pre_gerrit, post_gerrit],
                                     color=colors,
                                     edgecolor='white',
                                     histtype='bar',
                                     bins=bins,
                                     range=fixup_range,
                                     normed=True,
                                     align='left',
                                     label=['Pre-Peer Code Review',
                                           'Post-Peer Code Review'])
    for bar in patches[0]:
        bar.set_hatch('/')
    for bar in patches[1]:
        bar.set_hatch('\\')
    ax.set_xlabel('Number of Fix-up Commits')
    ax.set_ylabel('Commit Percentage')
    ax.set_xlim(fixup_range[0] + 1 - 0.5, fixup_range[1] + 0.5)
    y_max = 0.18
    ticklocs = np.linspace(0.0, y_max, 5)
    ax.set_yticks(ticklocs)
    ax.set_yticklabels([str(int(100*ii)) for ii in ticklocs])
    ax.set_ylim(0.0, y_max)

    with open('fix_up_bins.json', 'wb') as fp:
        fix_up_bins = {}
        fix_up_bins['single_pre'] = '{0:0.3g}'.format(percent[0][1] * 100)
        fix_up_bins['single_post'] = '{0:0.3g}'.format(percent[1][1] * 100)
        json.dump(fix_up_bins, fp)

    ax.legend()
    if outputfile:
        fig.savefig(outputfile)
    else:
        plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] +
              ' <PreGerrit.pkl> <PostGerrit.pkl> [output_file.eps]')
        sys.exit(1)

    with open(sys.argv[1], 'rb') as fp:
        pre_gerrit = pickle.load(fp)[0]
        pre_gerrit = [vv for vv in pre_gerrit.itervalues()]
        pre_gerrit = np.array(pre_gerrit)
    with open(sys.argv[2], 'rb') as fp:
        post_gerrit = pickle.load(fp)[0]
        post_gerrit = [vv for vv in post_gerrit.itervalues()]
        post_gerrit = np.array(post_gerrit)
    if len(sys.argv) > 3:
        outputfile = sys.argv[3]
        dirname = os.path.dirname(outputfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    else:
        outputfile = None
    plot_fixups(pre_gerrit, post_gerrit, outputfile)
