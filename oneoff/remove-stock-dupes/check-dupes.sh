source helpers.sh
dupes_f=$RANDOM.dupes
bash mark-dupes.sh > $dupes_f
{
  echo "Comparing stock reports and stock transactions for consistency"
  echo "If you see nothing but 0 below, you're ok:"
  diff <(cat $dupes_f | unpad-psql-table | cut -d'|' -f2 |
    rows-to-tuple-tuple | render-sql-template-from-rows fetch-transactions-for-reports.sql |
    psql_commcarehq | remove-header-and-footer | unpad-psql-table |
    sort) <(
  cat $dupes_f | cut -d' ' -f2 |
    sort)
  echo $?
}
rm $dupes_f
