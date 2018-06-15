#!/usr/bin/python
"""
Convert profile file such as that produced by `dimagi.utils.decorators.profile`
to a human-readable text file.
"""
import argparse
import pstats

DEFAULT_LIMIT = 200


def profile(filename, limit=DEFAULT_LIMIT, output=None, print_callers=False):
    output = output or filename + ".txt"
    with open(output, 'w') as f:
        print("loading profile stats for %s" % filename)
        stats = pstats.Stats(filename, stream=f)

        stats.sort_stats('cumulative', 'calls').print_stats(limit)
        if print_callers:
            stats.print_callers(limit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert profile to readable format')
    parser.add_argument('path', help="Path to profile file")
    parser.add_argument('-l', '--limit', type=int, default=DEFAULT_LIMIT, help='Limit the number of output lines')
    parser.add_argument('-c', '--callers', action='store_true', help='Also print the callers list')
    parser.add_argument('-o', '--output', help='Store the result in this output file')

    args = parser.parse_args()

    profile(args.path, args.limit, args.output, args.callers)
