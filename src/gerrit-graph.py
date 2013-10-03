#!/usr/bin/env python

"""Do a graph visualization of the Gerrit reviews."""

import collections
import json
import os
import sys

import networkx as nx

class hashdict(dict):
    """
    hashable dict implementation, suitable for use as a key into
    other dicts.

        >>> h1 = hashdict({"apples": 1, "bananas":2})
        >>> h2 = hashdict({"bananas": 3, "mangoes": 5})
        >>> h1+h2
        hashdict(apples=1, bananas=3, mangoes=5)
        >>> d1 = {}
        >>> d1[h1] = "salad"
        >>> d1[h1]
        'salad'
        >>> d1[h2]
        Traceback (most recent call last):
        ...
        KeyError: hashdict(bananas=3, mangoes=5)

    based on answers from
       http://stackoverflow.com/questions/1151658/python-hashable-dicts

    """
    def __key(self):
        return tuple(sorted(self.items()))
    def __repr__(self):
        return "{0}({1})".format(self.__class__.__name__,
            ", ".join("{0}={1}".format(
                    str(i[0]),repr(i[1])) for i in self.__key()))

    def __hash__(self):
        return hash(self.__key())
    def __setitem__(self, key, value):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def __delitem__(self, key):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def clear(self):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def pop(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def popitem(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def setdefault(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def update(self, *args, **kwargs):
        raise TypeError("{0} does not support item assignment"
                         .format(self.__class__.__name__))
    def __add__(self, right):
        result = hashdict(self)
        dict.update(result, right)
        return result


def reviewer_graph(changes):
    # TODO: temp for efficiency
    changes = changes[:100]

    # Nodes are contributors identified by name and email
    contributors = set()
    for change in changes:
        contributors.add(hashdict(change['owner']))

    # Node attribute -- number of changes created
    created = collections.Counter({cc: 0 for cc in contributors})
    for change in changes:
        created[hashdict(change['owner'])] += 1

    # Node attribute -- number of change reviews
    reviewed = collections.Counter({cc: 0 for cc in contributors})
    for change in changes:
        for patch_set in change['patchSets']:
            for approval in patch_set.get('approvals', []):
                reviewed[hashdict(approval['by'])] += 1

    # Add the nodes to the graph
    graph = nx.Graph()
    for contributor in contributors:
        graph.add_node(contributor,
                       created=created[contributor],
                       reviewed=reviewed[contributor])

    # Edges are reviews with weights by count and accumulated_value
    review_counts = collections.Counter()
    review_accumulated_values = collections.Counter()
    for change in changes:
        owner = hashdict(change['owner'])
        for patch_set in change['patchSets']:
            for approval in patch_set.get('approvals', []):
                reviewer = hashdict(approval['by'])
                review_counts[(reviewer, owner)] += 1
                review_accumulated_values[(reviewer, owner)] += \
                    int(approval['value'])

    for edge in review_counts.keys():
        graph.add_edge(*edge,
                       count=review_counts[edge],
                       accumulated_value=review_accumulated_values[edge])

    return graph


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] +
              ' <gerrit_data.json> [output_file.eps]')
        sys.exit(1)

    gerrit_data = sys.argv[1]
    with open(gerrit_data, 'r') as fp:
        data = json.load(fp)
    if len(sys.argv) > 2:
        outputfile = sys.argv[2]
        dirname = os.path.dirname(outputfile)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    else:
        outputfile = None

    graph = reviewer_graph(data['changes'])
