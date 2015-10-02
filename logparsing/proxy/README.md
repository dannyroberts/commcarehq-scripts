To get a date range of the logs run

```bash
python daterange.py 2015-09-01..2015-09-15 < production_commcare-nginx_access.log
```

or if you have more than one log to look through,

```bash
cat production_commcare-nginx_access.log* | python daterange.py 2015-09-01..2015-09-15
```

though be warned it's not super efficient and can take a while:
it'll scan all the logs and match them line by line.
