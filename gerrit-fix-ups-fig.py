#!/usr/bin/env python

import pickle
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcdefaults()
mpl.rcParams['axes.labelsize'] = 'x-large'
mpl.rcParams['xtick.labelsize'] = 'large'
mpl.rcParams['ytick.labelsize'] = 'large'
mpl.rcParams['legend.fontsize'] = 'x-large'
mpl.rcParams['figure.dpi'] = 900

def plot_fixups(pre_gerrit, post_gerrit, outputfile=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    fixup_range = (0, 6)
    bins = fixup_range[1]
    percent, bins, patches = ax.hist([pre_gerrit, post_gerrit],
            bins=bins,
            range=fixup_range,
            normed=True,
            align='left',
            label=['Pre-Peer Code Review', 'Post-Peer Code Review'])
    for bar in patches[0]:
        bar.set_hatch('/')
    for bar in patches[1]:
        bar.set_hatch('\\')
    ax.set_xlabel('Number of Fix-up Commits')
    ax.set_ylabel('Commit Percentage')
    ax.set_xlim(fixup_range[0] - 0.5, fixup_range[1] + 0.5)
    ax.set_yticklabels([str(int(100*ii)) for ii in np.linspace(0.0, 1.0, 6)])
    ax.set_ylim(0.0, 1.0)

    ax.legend()
    if outputfile:
        fig.savefig(outputfile)
    else:
        plt.show()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: ' + sys.argv[0] + ' <PreGerrit.pkl> <PostGerrit.pkl> [output_file.eps]')
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
    else:
        outputfile = None
    plot_fixups(pre_gerrit, post_gerrit, outputfile)
