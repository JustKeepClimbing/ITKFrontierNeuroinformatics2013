#!/usr/bin/env python

"""Download data from the Gerrit server and save to a json file.

Example::

  gerrit-stats.py -p 22 alice@review.source.kitware.com 'project:ITK limit:100' output.json

"""

import argparse
import json
import subprocess


def get_changes(host, port, query):
    """Download the changes from the Gerrit server and return the JSON data
    structure."""
    def call_server(query, resume=None):
        ssh_call = ['ssh', '-p', str(port), host, 'gerrit', 'query',
                    '--format=JSON', '--all-approvals']
        ssh_call.extend(query.split())
        if resume:
            ssh_call.append(resume)
        return subprocess.check_output(ssh_call)
    query_results = call_server(query)
    query_results = query_results.split('\n')
    retrieval_stats = json.loads(query_results[-2])
    row_count = retrieval_stats['rowCount']
    runtime = retrieval_stats['runTimeMilliseconds']
    print('\nNumber of changes retrieved: ' + str(row_count))
    print('Time for retrieval [msec]:   ' + str(runtime))
    query_results = query_results[:-2]
    # There is a limit of 500.
    def results_to_json(results):
        results = ','.join(results)
        json_changes = '{"changes":['
        json_changes += results
        json_changes += ']}'
        json_changes = json.loads(json_changes)
        return json_changes

    while retrieval_stats['rowCount'] == 500:
        resume = 'resume_sortkey:' + results_to_json(query_results)['changes'][-1]['sortKey']
        print(resume)
        next_results = call_server(query, resume)
        next_results = next_results.split('\n')
        retrieval_stats = json.loads(next_results[-2])
        row_count += retrieval_stats['rowCount']
        runtime = retrieval_stats['runTimeMilliseconds']
        print('\nNumber of changes retrieved: ' + str(row_count))
        print('Time for retrieval [msec]:   ' + str(runtime))
        next_results = next_results[:-2]
        query_results.extend(next_results)
    query_results = ','.join(query_results)

    json_changes = '{"changes":['
    json_changes += query_results
    json_changes += ']}'
    json_changes = json.loads(json_changes)
    return json_changes


def save_to_file(jsondata, filename):
    with open(filename, 'w') as fp:
        json.dump(jsondata, fp)


def main(args):
    changes = get_changes(args.host, args.port, args.query)
    save_to_file(changes, args.outputfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', '-p', type=int, default=29418)
    parser.add_argument('host', help='Host for the Gerrit Code Review instance.')
    parser.add_argument('query',
        help='Gerrit query to select changes.  See http://gerrit.googlecode.com/svn/documentation/2.2.1/user-search.html')
    parser.add_argument('outputfile', help='Output JSON file.')
    args = parser.parse_args()
    main(args)
