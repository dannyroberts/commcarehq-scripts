To update https://docs.google.com/spreadsheets/d/1GD7mdymlRVZ6pvDINw9dh8IybExWaOVoH6SonYjyhoY/edit#gid=2052320559
run

```bash
bash count-docs.sh ${cloudant-username} > tmp
```

Paste the current list of doc types into prev-doctypes (one per line),
and then run 

```bash
python merge-counts.py prev-doctypes tmp
```

You should be able to paste the output next to the current table, make sure the doc types line up with the previous ones
(I used an `=EQ({new doc type cell}, {old doc type cell})` column make shifted the previous one around until they all
came to to `TRUE`)
