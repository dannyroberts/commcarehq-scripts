## Setup
```bash
mkvirtualenv cloudant-rewind
pip install -r pip-requirements.txt
```

## Running
Put the doc `_id`s of the pillowtop checkpoints you want to scan
in `pillow_checkpoint_ids`, one per line, ending with a new line.

You can get an idea of which ones you want to reset
by running the following on hqdb0.

In [1]: from pillowtop.utils import get_all_pillows

In [2]: for pillow in get_all_pillows():
   ...:     print pillow.get_checkpoint()

Copy the output (one checkpoint doc per line, ending with a new line) into a file named checkpoint_docs.txt. Then run the following:

```bash
while read line; do echo $line | jsawk 'return this._id + " " + this.seq'; done < checkpoint_docs.txt | sed 's/^.*\.\([A-Z][A-Za-z]*Pillow\)[^ ]* \([0-9]*\)-.*$/\2 \1/' | sort -n
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
The first few will have checkpoint numbers significantly smaller than the rest. In this example it's the first 5 that are the problem. Based on that run a command like the following

```bash
while read line; do echo $line | jsawk 'return this._id'; done < checkpoint_docs.txt | grep -E 'XFormPillow|FormDataPillow|CasePillow|CaseDataPillow|ReportCasePillow' > pillow_checkpoint_ids
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
