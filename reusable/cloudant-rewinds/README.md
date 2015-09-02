## Setup
```bash
mkvirtualenv cloudant-rewind
pip install -r pip-requirements.txt
```

and install jsawk. On a Mac with Homebrew, that should be `brew install jsawk`.

## Running
Put the doc `_id`s of the pillowtop checkpoints you want to scan
in `pillow_checkpoint_ids`, one per line, ending with a new line.

You can get an idea of which ones you want to reset
by running the following on hqdb0.

```python
In [1]: from pillowtop.utils import get_all_pillows
In [2]: for pillow in get_all_pillows():
   ...:     print pillow.get_checkpoint()
```

Copy the output (one checkpoint doc per line, ending with a new line) into a file named checkpoint_docs.txt. Then run the following:

```bash
./extract_seq.py -f checkpoint_docs.txt
```

The output may look something like

```
22340210 XFormPillow
37238996 FormDataPillow
38161542 CasePillow
53780801 CaseDataPillow
53963197 ReportCasePillow
60009683 UserPillow
60067650 DomainPillow
60073019 GroupPillow
...
```
The first few will have checkpoint numbers significantly smaller than the rest. Those are the pillows that are in a rewind state and need to be reset to a reasonable `seq`. In this example it's the first 5 that are the problem. Based on that run a command like the following

```bash
./extract_seq.py -f checkpoint_docs.txt -l5 --id_only > pillow_checkpoint_ids
```

to pull just the full checkpoint _ids for the pillows you want.

Once you have your pillow ids in `pillow_checkpoint_ids`, run the following:

```bash
bash find_most_recent_good_checkpoint.sh 55000000 https://commcarehq.cloudant.com/commcarehq < pillow_checkpoint_ids | tee checkpoints_to_use.txt
```

`checkpoints_to_use.txt` will now contain the historical revisions
whose sequence id is greater than 55000000. Each alternating line is
(1) the doc `_id` (2) the historical revision.

## Troubleshooting

If it doesn't go right the first time, and you get a repeated error, this may have to do with the fact that each request is cached in a file to speed things up if you need to run this multiple times. To start with a clean slate, just run `rm *.cache`.

If `find_most_recent_good_checkpoint.sh` hits an infinite loop, this may be because CouchDB cannot find a revision with that high of a sequence id (in the example it's 55000000). CouchDB regularly compacts documents and removes revisions. If this is the case, you may be able to use a `seq` id from another search. The `seq` ids are from Cloudant so can use `seq` ids from other pillows. Be careful to make sure that that pillow has indeed seen that `seq` id, else the pillow will skip documents.
