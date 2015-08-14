## Setup
```bash
mkvirtualenv cloudant-rewind
pip install -r pip-requirements.txt
```

## Running
Put the doc `_id`s of the pillowtop checkpoints you want to scan
in pillow_checkpoint_ids, one per line, ending with a new line.

```bash
bash find_most_recent_good_checkpoint.sh 55000000 https://commcarehq.cloudant.com/commcarehq < pillow_checkpoint_ids | tee checkpoints_to_use.txt
```

`checkpoints_to_use.txt` will now contain the historical revisions
whose sequence id is greater than 55000000. Each alternating line is
(1) the doc `_id` (2) the historical revision.
