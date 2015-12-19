import csv
import re
import sh
import sys
from collections import Counter, namedtuple

LogInfo = namedtuple("LogInfo", "earliest_commit latest_commit num_commits")


def parse_author(output):
    return re.match(r"^.*[(]([a-zA-Z ]+)\s*20.*$", output).groups()[0].strip()


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
    command = filename.split("/")[-1].split(".py")[0]
    log_info = get_log_info(filename)
    return (
        command,
        filename,
        log_info.num_commits,
        log_info.earliest_commit,
        log_info.latest_commit,
        get_authors(filename),
    )


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
    files = [name.strip() for name in sh.find()
            if "management/commands" in name
            and "__init__" not in name
            and "submodules" not in name
            and ".py" in name]

    with open('mgmt_cmd_info.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            "Command",
            "File Name",
            "Commits",
            "First Commit",
            "Last Commit",
            "Authors",
            "We need this one (initial)",
            "This can definitely be deleted",
            "I'll see if this can be deleted",
        ])
        for filename in with_progress_bar(files):
            writer.writerow(get_row(filename))
