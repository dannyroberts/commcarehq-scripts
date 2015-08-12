To run this do:

```bash
bash pull-received-on-dates.sh https://username:****@dbname.cloudant.com > received_on_lookup
bash generate-SQL.sh < received_on_lookup
```

or of course you can do them together with

```bash
bash pull-received-on-dates.sh https://username:****@dbname.cloudant.com | bash generate-SQL.sh
```

Either way the output will look something like this:

```
BEGIN;
UPDATE stock_stockreport SET server_date = '2015-08-01T01:12:12.123456Z' WHERE form_id = 'c77e7a2cfd1e42e2a37ab60fcdc06d3d';
UPDATE stock_stockreport SET server_date = '2014-11-03T22:01:14.123456Z' WHERE form_id = '88bd97328fd8453db291fc7f2615259b';
...
END;
```

which you can copy directly into psql.
