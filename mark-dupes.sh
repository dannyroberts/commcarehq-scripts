function psql_commcarehq() {
  psql $PSQL_ARGS commcarehq
}

function remove-header-and-footer() {
  sed 1,2d | sed '$d' | sed '$d'
}

function get-unique-duplicates() {
  uniq -c | grep '^   [^1]' | cut -c7-
}

function rows-to-tuple-tuple() {
  sed 's/^\(.*\)$/'"('\1')/" | sed 's/ *| */'"','/g" | python -c "import sys; print '(' + ','.join(sys.stdin.readlines()) + ')'"
}

function render-sql-template-from-rows() {
  python -c 'import sys; print open("'"$1"'").read().format(rows=sys.stdin.read()),'
}
function mark-duplicates() {
  while read line
  do
    CURRENT_LINE=$(echo $line | cut -d'|' -f2-)
    if [[ $CURRENT_LINE = $PREV_LINE ]]
    then
      echo '✗' $line
    else
      echo '✓' $line
    fi
    PREV_LINE=$CURRENT_LINE
  done
}
function pull-id-field-from-dupe-rows() {
  grep '^✗' | cut -d' ' -f2
}

psql_commcarehq < select-dupe-fields.sql | remove-header-and-footer |
  get-unique-duplicates |
  rows-to-tuple-tuple | render-sql-template-from-rows select-rows-with-ids.sql |
  psql_commcarehq | remove-header-and-footer |
  mark-duplicates
