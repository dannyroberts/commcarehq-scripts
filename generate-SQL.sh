function generate-SQL() {
  form_id=$1
  server_date=$2
  echo UPDATE stock_stockreport SET server_date = \'$server_date\' WHERE form_id = \'$form_id\'\;
}

echo 'BEGIN;'
grep ' ' received_on_lookup | while read line
do
  generate-SQL $line
done
echo 'END;'
