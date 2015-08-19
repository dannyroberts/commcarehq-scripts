bash mark-dupes.sh |
  pull-id-field-from-dupe-rows |
  rows-to-tuple-tuple | render-sql-template-from-rows delete-rows-by-id.sql |
  psql commcarehq | remove-header-and-footer
