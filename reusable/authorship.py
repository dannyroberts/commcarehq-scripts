"""
Output git authorship information about a list of files.

Example usage:
    $ cd path/to/repository
    $ find . | grep "management/commands" | grep -v "__init__" | grep -v "submodules" | grep ".py$" | python path/to/authorship.py --csv

TODOs:
  How can I re.search for unicode characters?
  How should I output a table format to the terminal?
"""
from argparse import ArgumentParser
import csv
import re
import sh
import sys
from collections import Counter, namedtuple

LogInfo = namedtuple("LogInfo", "earliest_commit latest_commit num_commits")


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--csv", action="store_true", help="Dump to a csv")
    args = parser.parse_args()

    filenames = [filename.strip() for filename in sys.stdin.readlines()]
    print "Found {} files".format(len(filenames))
    if args.csv:
        with open("authorship.csv", 'w') as f:
            dump_info(with_progress_bar(filenames), f)
    else:
        dump_info(filenames, sys.stdout)


def parse_author(output):
    return re.search(r"[(]([a-zA-Z ]+)\s*20\d{2}", output).groups()[0].strip()


def get_authors(filename):
    raw_output = sh.git.blame(filename, _env={'PAGER': '/bin/cat'})
    author_by_line = filter(None, map(parse_author, raw_output))
    author_counts = sorted(Counter(author_by_line).items(),
                           key=lambda (author, count): count,
                           reverse=True)
    return " - ".join("{} ({})".format(name, count)
                      for name, count in author_counts)


def get_log_info(filename):
    raw_output = sh.git.log("--pretty=%ad", "--date=short", filename,
                            _env={'PAGER': '/bin/cat'})
    dates = sorted(raw_output.split())
    return LogInfo(
        earliest_commit=dates[0],
        latest_commit=dates[-1],
        num_commits=len(dates),
    )


def get_row(filename):
    log_info = get_log_info(filename)
    return (
        filename,
        log_info.num_commits,
        log_info.earliest_commit,
        log_info.latest_commit,
        get_authors(filename),
    )


def dump_info(filenames, fileobj):
    writer = csv.writer(fileobj)
    writer.writerow([
        "File Name",
        "Commits",
        "First Commit",
        "Last Commit",
        "Authors",
    ])
    for filename in filenames:
        # print filename
        writer.writerow(get_row(filename))


def with_progress_bar(iterable):
    length = len(iterable)
    checkpoints = {length*i/30 for i in range(length)}
    print 'Starting [' + ' '*30 + ']',
    print '\b'*32,
    sys.stdout.flush()
    for i, x in enumerate(iterable):
        yield x
        if i in checkpoints:
            print '\b.',
            sys.stdout.flush()
    print '\b]  Done!',


if __name__ == "__main__":
    main()
