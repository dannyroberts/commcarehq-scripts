#!/usr/bin/env python
# Usage:
#   ./extract_seq.py checkpoint_docs.txt

import json
import re
import sys
import argparse

name_rx = re.compile('^.*\.([A-Z][A-Za-z]*Pillow)')


def get_docs(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()


def extract_doc_id_seq(doc, full_ids=False):
    doc = doc.replace("'", '"')
    doc_json = json.loads(doc)
    full_id = doc_json['_id']
    id = full_id if full_ids else name_rx.match(full_id).group(1)
    seq = doc_json['seq'].split('-')[0]
    return id, seq


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process pillow checkpoints.')
    parser.add_argument('-f', '--file', default='checkpoint_docs.txt', help='Path to file containing checkpoint docs')
    parser.add_argument('-l', '--limit', type=int)
    parser.add_argument('--id_only', dest='id_only', action='store_true',
                       help='Only print out the full IDs')

    args = parser.parse_args()
    file_path = args.file
    limit = args.limit
    ids_only = args.id_only

    docs = get_docs(file_path)
    id_seq = sorted([extract_doc_id_seq(doc, ids_only) for doc in docs], key=lambda x: x[1])
    if limit:
        id_seq = id_seq[:limit]
    for doc_id, seq in id_seq:
        if ids_only:
            print doc_id
        else:
            print '{} {}'.format(seq, doc_id)
