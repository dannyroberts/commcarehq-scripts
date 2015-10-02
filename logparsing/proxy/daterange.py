import datetime


PROXY_DATETIME_FORMAT = '%d/%b/%Y:%H:%M:%S'
INPUT_DATETIME_FORMATS = ['%Y-%m-%dT%H:%M:%SZ', '%Y-%m-%d']

def _get_datetime_string_from_line(line):
    try:
        return line.split('[')[1].split(' ')[0]
    except IndexError:
        raise ValueError(line)


def _parse_proxy_datetime(dt_string):
    return datetime.datetime.strptime(dt_string, PROXY_DATETIME_FORMAT)


def get_datetime_from_line(line):
    dt_string = _get_datetime_string_from_line(line)
    return _parse_proxy_datetime(dt_string)


def parse_input_datetime(dt_string):
    if not dt_string:
        return None
    for fmt in INPUT_DATETIME_FORMATS:
        try:
            return datetime.datetime.strptime(dt_string, fmt)
        except ValueError:
            pass
    else:
        raise ValueError(dt_string)


def main(args, stdin):
    start_string, end_string = args[1].split('..')
    start = parse_input_datetime(start_string)
    end = parse_input_datetime(end_string)
    for line in stdin:
        dt = get_datetime_from_line(line)
        if start <= dt < end:
            print line,

if __name__ == '__main__':
    import sys
    main(sys.argv, sys.stdin)
