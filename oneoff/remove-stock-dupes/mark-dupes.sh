source helpers.sh
psql_commcarehq < select-dupe-fields.sql | remove-header-and-footer |
  get-unique-duplicates |
  rows-to-tuple-tuple | render-sql-template-from-rows select-rows-with-ids.sql |
  psql_commcarehq | remove-header-and-footer |
  mark-duplicates 2 |
  cat
