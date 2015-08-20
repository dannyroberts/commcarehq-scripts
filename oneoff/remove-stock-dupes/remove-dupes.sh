source helpers.sh
bash mark-dupes.sh |
  pull-report-id-field-from-dupe-rows |
  rows-to-tuple-tuple | render-sql-template-from-rows delete-rows-by-id.sql |
  psql_commcarehq | remove-header-and-footer |
  cat
