#!/usr/bin/env python

"""
gather_profile_stats.py /path/to/dir/of/profiles
Only works with cProfile stats
"""
import glob
import os
import pstats
import argparse


def gather_stats(search_path, patterns=None, output=None, delete=False):
    paths = []
    output = output or os.path.join(search_path, 'aggregate_profile.prof')

    for pattern in patterns:
        for path in glob.glob1(search_path, pattern):
            paths.append(os.path.join(search_path, path))

    if output in paths:
        print("Output file included in matching input files. Use '--output' to specify a different output file path.")
        return

    print('Processing paths: {}'.format('\n'.join(paths)))
    prof = pstats.Stats(*paths)

    if delete:
        for path in paths:
            os.unlink(path)

    print("Writing output to %s" % output)
    prof.dump_stats(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Aggregate cProfile dumps')
    parser.add_argument('path', help="Path to look for profile files")
    parser.add_argument('-p', '--pattern', nargs='+', default=['*.prof'],
                        help="Glob patterns to use to match files. Defaults to '*.prof'")
    parser.add_argument('-o', '--output', help='Store the result in this output file')
    parser.add_argument('--delete', action='store_true', help='Delete files once processed')

    args = parser.parse_args()
    gather_stats(args.path, patterns=args.pattern, output=args.output, delete=args.delete)
