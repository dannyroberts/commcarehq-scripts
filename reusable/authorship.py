"""
Output git authorship information about a list of files.  Accepts a stream of
filenames, like that produced by `$ git ls-files` or `$ find`.

Example usage:
    $ cd path/to/repository
    $ git ls-files | grep "management/commands" | grep -v "__init__" | grep ".py$" | python path/to/authorship.py --csv
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import Counter, namedtuple
from unidecode import unidecode
import csv
import re
import sh
import sys

LogInfo = namedtuple("LogInfo", "earliest_commit latest_commit num_commits")


def main():
    parser = ArgumentParser(description=__doc__, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("--csv", action="store_true", help="Dump to a csv")
    args = parser.parse_args()

    filenames = [filename.strip() for filename in sys.stdin.readlines()]
    print "Found {} files".format(len(filenames))
    if args.csv:
        with open("authorship.csv", 'w') as f:
            writer = csv.writer(f)
            for row in with_progress_bar(get_rows(filenames), len(filenames)):
                writer.writerow(row)
    else:
        for filename, commits, first, last, authors in get_rows(filenames):
            if len(filename) > 60:
                filename = "...{}".format(filename[-57:])
            print "{:<60} {:>10} {:^14}{:^14} {}".format(
                filename, commits, first, last, authors)


def parse_author(output):
    match = re.search(r"[(]([\w ]+)\s*20\d{2}", output, re.UNICODE)
    if not match:
        return
    return unidecode(match.groups()[0].strip())


def get_authors(filename):
    raw_output = sh.git.blame(filename, _env={'PAGER': '/bin/cat'})
    author_by_line = filter(None, map(parse_author, raw_output))
    author_counts = sorted(Counter(author_by_line).items(),
                           key=lambda (author, count): count,
                           reverse=True)
    return " - ".join(u"{} ({})".format(name, count)
                      for name, count in author_counts)


def get_log_info(filename):
    raw_output = sh.git.log("--pretty=%ad", "--date=short", "--since=2010-09-10",
                            filename, _env={'PAGER': '/bin/cat'})
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


def get_rows(filenames):
    yield [
        "File Name",
        "Commits",
        "First Commit",
        "Last Commit",
        "Authors",
    ]
    for filename in filenames:
        yield get_row(filename)


def with_progress_bar(iterable, length):
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
