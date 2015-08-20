 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import sys
import requests
import hashlib
import json
import logging
import re
import functools

logging.basicConfig(level=logging.DEBUG)

def get_cachefile(url):
    return hashlib.md5(url).hexdigest() + '.cache'

def cache_get(url):
    cachefile = get_cachefile(url)
    try:
        logging.info('Using cachefile {}'.format(cachefile))
        with open(cachefile, 'r') as f:
            return json.loads(f.read())
    except IOError:
        response = requests.get(url)
        response_json = response.json()
        with open(cachefile, 'w') as f:
            f.write(response.content)
            return response_json

def get_seq_int(checkpoint_doc):
    return int(checkpoint_doc['seq'].split('-')[0])


def scan_checkpoint_docs(urls, minimum_seq_int):
    """
    try first, second, fourth, eighth etc. urls until seq >= minimum_seq_int
    then binary search for earliest matching rev
    """
    last_index = None
    index = 0
    ceiling = len(urls) - 1
    matched = False
    candidate = None

    def get_seq(index):
        url = urls[index]
        checkpoint_doc = cache_get(url)
        seq = get_seq_int(checkpoint_doc)
        return seq, checkpoint_doc

    logging.info('Estimating range')

    def log_match(index, seq, match):
        if match:
            logging.info(u'{} @ {} ✓'.format(index, seq))
        else:
            logging.info(u'{} @ {} ✗'.format(index, seq))

    while not matched:
        seq, checkpoint_doc = get_seq(index)
        if seq >= minimum_seq_int:
            log_match(index, seq, True)
            candidate = index, seq, checkpoint_doc
            matched = True
        else:
            log_match(index, seq, False)
            matched = False
            last_index, index = index, (index + 1) * 2 - 1
            if index > ceiling:
                index = ceiling

    if not last_index:
        return checkpoint_doc
    logging.info('Starting binary search')
    range_start = last_index
    range_end = index
    tried_indexes = set()
    while range_start != range_end:
        index = int((range_start + range_end) / 2)
        if index in tried_indexes:
            break
        seq, checkpoint_doc = get_seq(index)
        if seq >= minimum_seq_int:
            log_match(index, seq, True)
            candidate = index, seq, checkpoint_doc
            range_end = index
            matched = True
        else:
            log_match(index, seq, False)
            matched = False
            range_start = index
        tried_indexes.add(index)
    index, seq, checkpoint_doc = candidate
    return checkpoint_doc

if __name__ == '__main__':
    minimum_seq_int = int(sys.argv[1])
    doc_url = sys.argv[2]
    revs = [line.strip('\n') for line in sys.stdin.readlines()]
    urls = [doc_url + '?rev=' + rev for rev in revs]

    print scan_checkpoint_docs(urls, minimum_seq_int)
